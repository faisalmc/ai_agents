#!/usr/bin/env python3
"""
Author: Faisal Chaudhry

Agent Router (Agent A Poller):
- Polls GitHub for new commits under doo/configs*/task-*
- Clones or updates the repo securely with token-based authentication
- Detects new file-level changes in the latest commit (diff changes only in last commit)
- Uses Agent A + OpenAI LLM to summarize configuration intent
- Posts JSON summary to Slack with config/task context

DEBUG logging is controlled by the DEBUG env var.
"""

import os
import time
import requests
import openai
import re
from slack_sdk import WebClient
from git import Repo, GitCommandError

from llm_clients.agent_a import summarize_changes
from llm_clients.llm_api import call_llm

# --- Configuration (via .env) ---
GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN", "").strip()
GITHUB_OWNER   = os.getenv("GITHUB_OWNER", "").strip()
GITHUB_REPO    = os.getenv("GITHUB_REPO", "").strip()
REPO_CLONE_DIR = os.getenv("REPO_CLONE_DIR", "/opt/tasks").strip()
POLL_INTERVAL  = int(os.getenv("POLL_INTERVAL", "60").strip())  # seconds
SLACK_TOKEN    = os.getenv("SLACK_BOT_TOKEN", "").strip()
SLACK_CHANNEL  = os.getenv("SLACK_CHANNEL", "#all-sp").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo").strip()

# --- Debug toggle ---
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")

# --- Github task folder ----
TASK_FOLDER_RE = re.compile(r"^doo/configs\.\d+(?:\.[^/]+)?/task-[^/]+/.+")

def dbg(msg: str):
    if DEBUG:
        print(f"[DEBUG] {msg}", flush=True)

# --- Initialize clients ---
openai.api_key = OPENAI_API_KEY
slack = WebClient(token=SLACK_TOKEN)

STATE_FILE = ".last_sha"

def get_last_sha():
    try:
        last = open(STATE_FILE).read().strip()
        dbg(f"last SHA loaded: {last}")
        return last
    except FileNotFoundError:
        dbg("no last SHA file found")
        return None

def set_last_sha(sha: str):
    with open(STATE_FILE, "w") as f:
        f.write(sha)
    dbg(f"last SHA updated to: {sha}")

def fetch_latest_commit():
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"sha": "main", "per_page": 1}
    dbg("Fetching latest commit from GitHub")
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    commits = r.json()
    if not commits:
        raise RuntimeError("No commits found in repo")
    latest = commits[0]
    dbg(f"Latest commit: {latest['sha']}")
    return latest

def detect_task_changes_in_commit(commit_sha):
    auth_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_OWNER}/{GITHUB_REPO}.git"
    # Mask token in logs
    try:
        masked = auth_url.replace(GITHUB_TOKEN, "****") if GITHUB_TOKEN else auth_url
    except Exception:
        masked = "****"
    dbg(f"using auth_url={masked}")

    if not os.path.isdir(REPO_CLONE_DIR):
        dbg(f"cloning repo into {REPO_CLONE_DIR}")
        try:
            Repo.clone_from(auth_url, REPO_CLONE_DIR)
        except GitCommandError as e:
            raise RuntimeError(f"Failed to clone repo: {e}")
    else:
        dbg(f"pulling updates into {REPO_CLONE_DIR}")
        try:
            repo = Repo(REPO_CLONE_DIR)
            origin = repo.remote(name="origin")
            origin.set_url(auth_url)
            origin.pull()
        except GitCommandError as e:
            raise RuntimeError(f"Failed to pull repo: {e}")

    changes = []
    repo = Repo(REPO_CLONE_DIR)
    dbg(f"examining commit {commit_sha}")
    try:
        files = repo.git.show("--name-only", "--pretty=", commit_sha).splitlines()
    except GitCommandError as e:
        dbg(f"Error during git show: {e}")
        return []

    if not files:
        dbg(f"No files found in commit {commit_sha}")
        return []

    # Only pass along device .txt files and show_cmds.ini
    ALLOWED_BASENAMES = {"show_cmds.ini"}
    ALLOWED_TXT_SUFFIX = (".txt",)

    dbg("Files changed in commit:")
    for path in files:
        dbg(f"  - {path}")
        if not TASK_FOLDER_RE.search(path):
            dbg("    → did NOT match TASK folder regex ❌")
            continue

        base = os.path.basename(path)
        if base.startswith("."):
            dbg("    → skip dotfile")
            continue

        if path.endswith(ALLOWED_TXT_SUFFIX) or base in ALLOWED_BASENAMES:
            dbg("    → matched TASK folder + allowed type ✅")
            changes.append((commit_sha, path))
        else:
            dbg("    → skip (not .txt or show_cmds.ini)")

    dbg(f"total changes detected: {len(changes)}")
    return changes

def resolve_slack_channel():
    """
    Resolve Slack channel ID safely.
    - If SLACK_CHANNEL already looks like an ID (C*/G*/D*), use it.
    - Else try to look it up (requires channels:read/groups:read).
    - On missing_scope or any error, fall back to the raw name.
    """
    raw = SLACK_CHANNEL.strip()
    if raw.startswith(("C", "G", "D")) and " " not in raw:
        dbg(f"Using provided channel ID: {raw}")
        return raw

    channel_name = raw.lstrip("#")
    try:
        resp = slack.conversations_list(types="public_channel,private_channel")
        channel_id = next((ch["id"] for ch in resp["channels"] if ch["name"] == channel_name), None)
        if channel_id:
            dbg(f"Resolved channel {channel_name} to ID {channel_id}")
            return channel_id
        dbg(f"Channel {channel_name} not found, using raw name")
        return raw
    except Exception as e:
        dbg(f"Failed to resolve channel ID (will use raw): {e}")
        return raw

SUMMARY_FEWSHOT = [
    {
        "role": "user",
        "content": "```json\n[{\"hostname\": \"A-PE-1\", \"role\": \"Provider-Edge\", \"config_intents\": [\"Enable segment routing\", \"Assign prefix-sid index\"]}]\n```"
    },
    {
        "role": "assistant",
        "content": (
            "*Executive Summary:*\n"
            "Configured segment routing and prefix-sid assignments across devices for traffic engineering.\n\n"
            "*Engineering Summary:*\n"
            "• A-PE-1:\n"
            "   - Enabled segment routing\n"
            "   - Assigned prefix-sid index"
        )
    }
]


def summarize_and_post(changes):
    tasks = {}
    for sha, path in changes:
        parts = path.split("/")
        if len(parts) >= 3:
            config_dir = parts[1]
            task_dir = parts[2]
            key = (config_dir, task_dir)
            tasks.setdefault(key, []).append((sha, path))

    slack_channel = resolve_slack_channel()
    channel_id_or_name = slack_channel

    # ----------------------------
    # Few-shot examples for summaries
    # ----------------------------
    SUMMARY_FEWSHOT = [
        {
            "role": "user",
            "content": """```json
[
  {
    "hostname": "A-ASBR-1",
    "role": "Provider-ASBR",
    "config_intents": [
      "Enable segment routing",
      "Configure MPLS preference for ISIS",
      "Set prefix-sid indexes on Loopback0"
    ]
  },
  {
    "hostname": "A-PE-1",
    "role": "Provider-Edge",
    "config_intents": [
      "Enable segment routing",
      "Configure microloop avoidance",
      "Assign prefix-sid indexes for IPv6"
    ]
  }
]
```"""
        },
        {
            "role": "assistant",
            "content": """*Executive Summary:*
This task will enable segment routing on 2 provider routers (ASBR and PE). 
The configuration will improve network resiliency and traffic engineering, 
support automated fast reroute, and prepare the MPLS core for future scaling.

*Engineering Summary:*
• A-ASBR-1:
   - Enable segment routing
   - MPLS preference configuration for ISIS
   - Prefix-sid assignment on Loopback0
• A-PE-1:
   - Enable segment routing
   - Configure microloop avoidance for ISIS
   - IPv6 prefix-sid assignment on Loopback0
"""
        }
    ]

    # ----------------------------
    # Updated system prompt
    # ----------------------------
    system_prompt = (
        "You are a senior network automation assistant.\n"
        "Given a JSON array of configuration intents for multiple devices, "
        "produce two summaries:\n\n"
        "1. Executive Summary – Future-looking, high-level summary for directors. "
        "Avoid technical jargon (e.g., prefix-sid, microloop). "
        "Include:\n"
        "   - Number and types of devices affected\n"
        "   - Purpose and expected business/operational benefits\n"
        "   - Use future tense (e.g., 'will configure', 'will enable')\n\n"
        "2. Engineering Summary – Technical, grouped by device or role. "
        "Use bullet points grouped by device or role. "
        "Keep it concise but technical.\n\n"
        "Output must be Slack-friendly formatted text with bold headers and bullet points."
    )

    github_base_url = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/tree/main"

    for (config_dir, task_dir), task_changes in tasks.items():
        dbg(f"Summarizing {len(task_changes)} changes for {config_dir} / {task_dir}")
        json_out = summarize_changes(task_changes)

        # --- Persist Agent-1 JSON into the task directory (latest only; remove old per-SHA files) ---
        import glob  # local import to avoid touching global imports

        task_root = os.path.join("/app/doo", config_dir, task_dir)
        os.makedirs(task_root, exist_ok=True)

        latest_json_path = os.path.join(task_root, "agent1_summary.json")

        # 1) Write/overwrite the latest pointer
        with open(latest_json_path, "w") as f:
            f.write(json_out)

        # 2) Clean up any old per-SHA snapshots (agent1_summary_<sha>.json)
        for old in glob.glob(os.path.join(task_root, "agent1_summary_*.json")):
            try:
                os.remove(old)
                dbg(f"[persist] Removed old snapshot: {old}")
            except Exception as e:
                dbg(f"[persist] Failed to remove {old}: {e}")

        dbg(f"[persist] Agent-1 summary (latest) written: {latest_json_path}")


        json_filename = f"{task_dir}-summary.json"
        json_path = os.path.join("/tmp", json_filename)
        with open(json_path, "w") as f:
            f.write(json_out)

        try:
            summary_prompt = [
                {"role": "system", "content": system_prompt},
                *SUMMARY_FEWSHOT,
                {"role": "user", "content": f"```json\n{json_out}\n```"}
            ]
            formatted_summary = call_llm(summary_prompt, temperature=0.0)

            # --- Optional: persist human-readable summary for audit/history ---
            brief_md_path = os.path.join(task_root, "agent1_brief.md")
            try:
                with open(brief_md_path, "w") as f:
                    f.write(f"# Agent-1 Summary for {task_dir}\n\n")
                    f.write(formatted_summary if formatted_summary else "_(empty)_")
                dbg(f"[persist] Human summary written: {brief_md_path}")
            except Exception as e:
                dbg(f"[persist] Failed writing agent1_brief.md: {e}")


        except Exception as e:
            dbg(f"Failed to generate exec/eng summary: {e}")
            formatted_summary = "_Could not generate Executive/Engineering summary._"

        # NEW: Construct push-configs hint message
        push_hint = (
            f"\n\n_To push these configs to devices, run:_\n"
            f"`/push-configs {config_dir} {task_dir}`"
        )

        slack_message = (
            f"📋 *Config Review Summary*\n"
            f"*Task:* `{task_dir}`\n"
            f"*Config Dir:* `{config_dir}`\n\n"
            f"{formatted_summary}\n\n"
            f"*A detailed JSON summary file (`{json_filename}`) has been attached for full reference.*\n\n"
            f"For detailed review, visit: {github_base_url}/doo/{config_dir}/{task_dir}"
            f"{push_hint}"   
        )

        slack.chat_postMessage(
            channel=channel_id_or_name,
            text=slack_message
        )

        try:
            with open(json_path, "rb") as f:
                slack.files_upload_v2(
                    channel=channel_id_or_name,
                    file=f,
                    title=f"{task_dir} JSON Summary",
                    filename=json_filename,
                    initial_comment="Full structured configuration intents (JSON):"
                )
        except Exception as e:
            dbg(f"Failed to upload JSON file: {e}")

        dbg(f"Posted summary and JSON file for {config_dir} / {task_dir} to Slack")


def poller_loop():
    dbg("starting poller_loop()")
    last_sha  = get_last_sha()
    print(f"[START] Polling every {POLL_INTERVAL}s (DEBUG={DEBUG})", flush=True)

    while True:
        try:
            latest_commit = fetch_latest_commit()
            latest_sha = latest_commit.get("sha")
            dbg(f"latest commit sha={latest_sha}")

            if last_sha is None:
                dbg("First run: syncing SHA without summary")
                set_last_sha(latest_sha)
                last_sha = latest_sha

            elif latest_sha != last_sha:
                dbg(f"New commit found: {latest_sha}, processing changes")
                changes = detect_task_changes_in_commit(latest_sha)
                dbg(f"changes list: {changes}")
                if changes:
                    summarize_and_post(changes)
                set_last_sha(latest_sha)
                last_sha = latest_sha
            else:
                dbg("No new commit detected.")

        except Exception as e:
            slack.chat_postMessage(
                channel=resolve_slack_channel(),
                text=f":warning: Poller error: {e}"
            )
            dbg(f"Caught exception: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poller_loop()


