# shared/push_core.py
"""
Core deployment logic for pushing CLI configs (Agent-2 shared module).

- No Slack/Bolt/threads here.
- Orchestrator and Agent-2 both import and call push_configs().
"""

import os
import re
import glob
import subprocess
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple

# Reuse the flexible error patterns (IOS / IOS-XR)
GENERIC_ERROR_PATTERNS = [
    r"%\s*Invalid input.*",
    r"%\s*Incomplete command.*",
    r"%\s*Ambiguous command.*",
    r"%\s*Unrecognized command.*",
    r"commit.*failed",
    r"config apply failed",
    r"syntax error",
    r"\^.*%.*input.*",  # caret marker with error
    r"%\s*Error.*",
    r"error:.*",
    r"ERROR:.*",
    r"command rejected",
    r"unknown command",
]

def _repo_paths(config_dir: str, task_dir: str) -> Tuple[str, str, str]:
    """
    Returns (repo_dir, script_path, log_dir)
    """
    repo_dir = os.path.join("/app/doo", config_dir)
    script_path = os.path.join(repo_dir, "push_cli_configs.py")
    log_dir = os.path.join(repo_dir, task_dir, "logs")
    return repo_dir, script_path, log_dir

def run_push_script(config_dir: str, task_dir: str, timeout: int = 300) -> Tuple[str, str, int]:
    """
    Execute push_cli_configs.py for the given task.

    Returns:
        stdout, stderr, returncode
    """
    repo_dir, script_path, _ = _repo_paths(config_dir, task_dir)
    cmd = ["python3", script_path, "--task", task_dir]

    print(f"[DEBUG] run_push_script: repo_dir={repo_dir} script={script_path} cmd={' '.join(cmd)}", flush=True)

    try:
        os.listdir(repo_dir)
    except Exception as e:
        err = f"[ERROR] Could not list repo_dir {repo_dir}: {e}"
        print(err, flush=True)
        return "", err, -1

    if not os.path.isfile(script_path):
        err = f"[ERROR] Script not found at: {script_path}"
        print(err, flush=True)
        return "", err, -1

    try:
        result = subprocess.run(
            cmd, cwd=repo_dir, capture_output=True, text=True, timeout=timeout
        )
        stdout, stderr, rc = result.stdout, result.stderr, result.returncode

        print(f"[DEBUG] Subprocess rc={rc}", flush=True)
        if stdout:
            print(f"[DEBUG] STDOUT (first 500 chars):\n{stdout[:500]}", flush=True)
        if stderr:
            print(f"[DEBUG] STDERR (first 500 chars):\n{stderr[:500]}", flush=True)

        # If success but no logs, warn
        if rc == 0:
            _, _, log_dir = _repo_paths(config_dir, task_dir)
            if not glob.glob(os.path.join(log_dir, "*.log")):
                print(f"[WARN] rc=0 but no log files in {log_dir}", flush=True)

        return stdout, stderr, rc

    except subprocess.TimeoutExpired:
        err = f"[ERROR] Script timed out after {timeout}s"
        print(err, flush=True)
        return "", err, -1
    except Exception as e:
        err = f"[ERROR] Exception during subprocess: {e}"
        print(err, flush=True)
        return "", err, -1

def basic_log_analysis(config_dir: str, task_dir: str) -> Tuple[List[Tuple[str, str]], List[str], str]:
    """
    Analyze logs for generic CLI/commit errors.

    Returns:
        results: list of (hostname, status) where status is "Success" or semicolon-joined issue list
        error_hosts: list of hostnames with errors
        log_dir: path to the logs directory
    """
    _, _, log_dir = _repo_paths(config_dir, task_dir)
    results: List[Tuple[str, str]] = []
    error_hosts: List[str] = []

    print(f"[DEBUG] basic_log_analysis: log_dir={log_dir}", flush=True)
    found_logs = glob.glob(os.path.join(log_dir, "*.log"))
    print(f"[DEBUG] Found log files: {found_logs}", flush=True)

    if not found_logs:
        results.append(("logs", "No .log files found. Check if push script ran correctly."))
        return results, error_hosts, log_dir

    for logfile in sorted(found_logs):
        hostname = os.path.basename(logfile).replace(".log", "")
        try:
            with open(logfile) as f:
                log = f.read()
        except Exception as e:
            results.append((hostname, f"Could not read log: {e}"))
            continue

        issues: List[str] = []

        for pattern in GENERIC_ERROR_PATTERNS:
            if re.search(pattern, log, re.IGNORECASE | re.MULTILINE):
                issues.append(f"Matched: {pattern}")
                print(f"[DEBUG] Matched error in {hostname}: {pattern}", flush=True)

        # caret + invalid input spanning lines
        if re.search(r"\s*\^\s*\n.*% Invalid input", log, re.IGNORECASE):
            issues.append("Caret Invalid Input Detected")
            print(f"[DEBUG] Detected caret pattern in {hostname}", flush=True)

        if issues:
            error_hosts.append(hostname)
            results.append((hostname, "; ".join(issues)))
        else:
            results.append((hostname, "Success"))

    return results, error_hosts, log_dir

def generate_summary_md(log_dir: str, output_path: str) -> None:
    """
    Concatenate all per-device .log files into a single markdown file.
    """
    print(f"[DEBUG] generate_summary_md: {output_path}", flush=True)
    try:
        with open(output_path, "w") as summary:
            for log_file in sorted(os.listdir(log_dir)):
                if log_file.endswith(".log"):
                    summary.write(f"## {log_file}\n\n")
                    with open(os.path.join(log_dir, log_file), "r") as lf:
                        content = lf.read()
                        summary.write("```\n")
                        summary.write(content)
                        summary.write("\n```\n\n")
    except Exception as e:
        print(f"[ERROR] Failed to generate summary markdown: {e}", flush=True)

def push_configs(config_dir: str, task_dir: str,
                 device_filter: Optional[List[str]] = None, # currently not applied to push_cli_configs.py
                 dry_run: bool = False) -> Dict[str, Any]:  # currently informational (not part of script)
    """
    Entry point used by both the orchestrator and Agent-2.

    Returns JSON:
    {
      "summary": "<string>",
      "per_device": [
        {"hostname": "<str>", "ok": <bool>, "details": "<str>"},
        ...
      ],
      "artifacts": {
        "log_dir": "<path>",
        "summary_md": "<path or None>",
      },
      "meta": {
        "task_id": "<str>",
        "config_dir": "<str>",
        "task_dir": "<str>",
        "timestamp_utc": "<YYYY-MM-DD HH:MM UTC>",
        "return_code": <int>
      }
    }
    """
    # TODO: If your push_cli_configs.py supports filtering/dry-run, add flags here.
    stdout, stderr, rc = run_push_script(config_dir, task_dir)

    results, error_hosts, log_dir = basic_log_analysis(config_dir, task_dir)

    success_hosts: List[str] = []
    per_device: List[Dict[str, Any]] = []
    errors: Dict[str, str] = {}

    for host, status in results:
        if status == "Success":
            success_hosts.append(host)
            per_device.append({"hostname": host, "ok": True, "details": status})
        else:
            errors[host] = status
            per_device.append({"hostname": host, "ok": False, "details": status})

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    summary_md_filename = "push_cli_configs-summary.md"
    summary_md_path = os.path.join(log_dir, summary_md_filename)

    # Build a concise human summary
    summary = (
        f"Task `{task_dir}` from `{config_dir}` | "
        f"OK: {len(success_hosts)} | ERR: {len(errors)} | "
        f"Log dir: {log_dir}"
    )


    # Always try to produce the markdown bundle
    if os.path.isdir(log_dir):
        generate_summary_md(log_dir, summary_md_path)
    else:
        summary_md_path = None

    artifacts = {
        "log_dir": log_dir,
        "summary_md": summary_md_path,
    }
    meta = {
        "config_dir": config_dir,
        "task_dir": task_dir,
        "timestamp_utc": timestamp,
        "return_code": rc,
    }

    # DEBUG: types/sanity before returning
    print(f"[DEBUG] return sanity: per_device={len(per_device)} items, "
          f"artifacts={artifacts}, meta={meta}", flush=True)

    return {
        "summary": summary,
        "per_device": per_device,
        "artifacts": artifacts,
        "meta": meta,
    }

    # # Always try to produce the markdown bundle
    # if os.path.isdir(log_dir):
    #     generate_summary_md(log_dir, summary_md_path)
    # else:
    #     summary_md_path = None

    # return {
    #     "summary": summary,
    #     "per_device": per_device,
    #     "artifacts": {...},
    #     "meta": {
    #         "config_dir": config_dir,
    #         "task_dir": task_dir,
    #         "timestamp_utc": timestamp,
    #         "return_code": rc,
    #     },
    # }