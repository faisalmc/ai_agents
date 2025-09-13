"""
Author: Faisal Chaudhry

Agent A:
- Builds structured prompts for summarizing task configuration files
- Extracts intents from .txt (config) and .ini (show command) files
- Assigns roles and provider/customer mapping based on filename
- Generates structured JSON for each host using an OpenAI LLM
"""

import os
import re
import glob
import json
from datetime import datetime

from shared.llm_api import call_llm 

# --- Local command memory roots ---
AGENT_KNOWLEDGE_ROOT = os.getenv("AGENT_KNOWLEDGE_ROOT", "/app/doo/_agent_knowledge")
LEXICON_ROOT = os.path.join(AGENT_KNOWLEDGE_ROOT, "lexicon")      # global, per-platform
OBSERVED_ROOT = os.path.join(AGENT_KNOWLEDGE_ROOT, "observed")    # per-task, from .ini

def _append_unique_lines(path: str, lines: list[str]):
    """Append new lines to a text file if they are not already present."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            existing = set(l.strip() for l in fh if l.strip())
    new = [l.strip() for l in lines if l.strip() and l.strip() not in existing]
    if new:
        with open(path, "a", encoding="utf-8") as fh:
            for l in new:
                fh.write(l + "\n")

_SHOW_LINE = re.compile(r"^\s*(show\s+.+)$", re.IGNORECASE)
def _extract_show_cmds_from_ini(text: str) -> list[str]:
    """Return all 'show ...' lines from an .ini blob."""
    out = []
    for raw in text.splitlines():
        m = _SHOW_LINE.search(raw)
        if m:
            out.append(m.group(1).strip())
    return out
# ---------- Deterministic context from filename ----------
def _provider_from_prefix(hostname_upper: str) -> str | None:
    # A-* -> Alpha, B-* -> Beta, C-* -> Charlie
    if hostname_upper.startswith("A-"): return "Alpha"
    if hostname_upper.startswith("B-"): return "Beta"
    if hostname_upper.startswith("C-"): return "Charlie"
    return None

def _role_from_hostname(hostname_upper: str) -> str | None:
    # maps tokens in the hostname to role
    # e.g., *-PE-*, *-P-*, *-ASBR-*, *-RR-*, *-CE-*
    if "-ASBR-" in hostname_upper: return "ASBR"
    if "-RR-"   in hostname_upper: return "Route-Reflector"
    if "-PE-"   in hostname_upper: return "Provider-Edge"
    if "-P-"    in hostname_upper: return "Provider"
    if "-CE-"   in hostname_upper: return "Customer-Edge"
    return None

def _customer_from_hostname(hostname_upper: str) -> str | None:
    # optional: map specific customer labels if your naming has them
    # (keep None for now — your earlier JSON uses null)
    return None

def _platform_hint_from_hostname(hostname_upper: str) -> str:
    """
    Project rule (your spec):
      • All *-CE-*  ==> Cisco IOS
      • All *-RR-*  ==> Cisco IOS
      • All others  ==> Cisco IOS-XR
    Encode as normalized tokens:
      'cisco-ios' or 'cisco-ios-xr'
    """
    if "-CE-" in hostname_upper or "-RR-" in hostname_upper:
        return "cisco-ios"
    return "cisco-ios-xr"

def _vendor_hint() -> str:
    # You said all are Cisco for now; keep this future-proof if multi-vendor arrives
    return "cisco"

def build_filename_context(basename: str) -> dict:
    """
    Build a small, deterministic context object to include with the prompt.
    LLM must copy these verbatim into output (we enforce via the system prompt).
    """
    hostname = os.path.splitext(basename)[0]
    hu = hostname.upper()

    return {
        "hostname": hostname,
        "provider": _provider_from_prefix(hu),
        "customer": _customer_from_hostname(hu),
        "role": _role_from_hostname(hu),
        "platform_hint": _platform_hint_from_hostname(hu),
        "vendor": _vendor_hint()
    }


def sanitize_lexicon(knowledge_root: str, platforms: list[str] | None = None):
    """
    Demote any lines in trusted lexicon that were never observed.
    Moves them into lexicon/_candidates/<platform>.txt.
    """
    import glob

    platforms = platforms or ["cisco-ios", "cisco-ios-xr"]
    for plat in platforms:
        trusted_path   = os.path.join(knowledge_root, "lexicon", f"{plat}.txt")
        candidates_path= os.path.join(knowledge_root, "lexicon", "_candidates", f"{plat}.txt")

        # Aggregate all observed 'show ...' lines
        observed_glob = os.path.join(knowledge_root, "observed", "**", "commands.txt")
        observed = set()
        for p in glob.glob(observed_glob, recursive=True):
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    for line in fh:
                        s = line.strip()
                        if s and s.lower().startswith("show "):
                            observed.add(s)
            except Exception:
                pass

        if not os.path.exists(trusted_path):
            continue

        keep, demote = [], []
        with open(trusted_path, "r", encoding="utf-8") as fh:
            for line in fh:
                cmd = line.rstrip("\n")
                if cmd in observed:
                    keep.append(cmd)
                else:
                    demote.append(cmd)

        if demote:
            os.makedirs(os.path.dirname(candidates_path), exist_ok=True)
            with open(candidates_path, "a", encoding="utf-8") as out:
                for cmd in demote:
                    out.write(cmd + "\n")
            with open(trusted_path, "w", encoding="utf-8") as out:
                for cmd in sorted(set(keep)):
                    out.write(cmd + "\n")
            dbg(f"[lexicon] demoted {len(demote)} unobserved lines → _candidates ({plat})")

# —————————————————————————————————————————————————————————
# Updated system prompt for individual file processing
# —————————————————————————————————————————————————————————
SYSTEM_PROMPT = """\
You are a Cisco Service Provider / Customer-Edge configuration assistant.
You will be given a Task name and a single file (configuration .txt OR operational checks .ini).

IMPORTANT:
• A small JSON "Context" may be provided. If present, you MUST copy its fields verbatim
  into your output (do not re-infer or override). These keys may include:
  Keys: {"hostname","provider","customer","role","platform_hint","vendor"}.
• When suggesting any show commands, you MUST align to platform_hint:
  - platform_hint == "cisco-ios"     → IOS-style CLI (e.g., 'show run | section ...', 'show ip ...')
  - platform_hint == "cisco-ios-xr"  → IOS-XR CLI (e.g., 'show running-config router ...', 'show route ...')
• Never mix platforms in suggested commands.

Your job is to emit ONE JSON object per file with:
- core identity (hostname, role, provider/customer, platform_hint, vendor),
- concise "config_intents" (natural language),
- a LIGHTWEIGHT, FLEXIBLE "expected_state" array for key signals (such as bgp, isis, mpls, sr, evpn, l2vpn, intf, ip, ...).
Keep the schema loose enough to cover new vendors/protocols without breaking.

For each signal in expected_state, split proposed show commands into two buckets:
  • suggested_show  → only commands that you are ≥0.75 confident AND match platform_hint
  • candidate_show  → any other ideas (lower confidence, unsure, or possibly wrong platform)

For each command, include metadata: { "cmd", "provenance", "confidence", "platform" }
  - provenance: "llm" (use this; do NOT guess "lexicon"/"ini"/"md" unless the command literally appears in this input file)
  - confidence: "high" (≥0.90), "med" (≈0.75–0.89), "low" (<0.75)
  - platform: repeat the platform you’re targeting, e.g. "cisco-ios-xr" or "cisco-ios"

Rules:

A. For .txt files (device configs):
   • Hostname = filename without extension (e.g. “A-PE-1.txt” → “A-PE-1”).
   • Decode X-ROLE-N:
     - If ROLE in {PE, P, ASBR, RR}, then X = SP (A=Alpha, B=Beta, C=Charlie).
     - If ROLE == CE, then X = Customer (B=Blue, S=Silver, R=Red, M=Magneto).
   • Extract the *design intent* behind the configuration into "config_intents" (not just CLI lines).
   • Group related lines into meaningful intents using declarative language.
   • Build a FLEXIBLE “expected_state” array (2–6 items max) per major signal (e.g., isis, bgp, mpls). 
     Each element is an observation target the NOC should later verify
     Each item:
     {
       "signal": <string> "<e.g., bgp|isis|mpls|sr|evpn|l2vpn|intf|ip|...>",
       "observation_goals": [ "list of checks in human terms derived from config (no invented facts)" ],
       "suggested_show": [
         { "cmd": "show ...", "provenance": "llm", "confidence": "high|med|low", "platform": "<platform_hint>" }
       ],
       "candidate_show": [
         { "cmd": "show ...", "provenance": "llm", "confidence": "high|med|low", "platform": "<platform_hint>", "note": "why not in suggested (e.g., confidence <0.75 or platform uncertainty)" }
       ]
     }
     Note:
     - "suggested_show": [IOS or IOS-XR commands that match platform_hint]
   • Put a command in suggested_show ONLY if:
       (confidence ≥ 0.75) AND (platform matches platform_hint).
        Otherwise, put it in candidate_show with a short note.
   • Do NOT invent device-specific values not present in config.


B. For show_cmds.ini:
   • This file contains commands for operational checks after configuration is applied.
   • Hostname = "Operational-Checks: show_cmds.ini"
   • Role = "validation-commands"
   • Each line is a "show" command.
   • Group them by protocol (e.g. ISIS, BGP, MPLS, SR, OSPF, etc.) if possible.
   • Emit:
     {
       "hostname": "Operational-Checks: show_cmds.ini",
       "role": "validation-commands",
       "checks": [
         { "intent": "human purpose", "command": "show ...", "protocol": "..." }
       ]
     }

Output:
• Respond ONLY with valid JSON (ONE object). No commentary outside JSON.

For device config (.txt):
{
  "hostname": "<from Context or filename>",
  "provider": "<from Context if present>",
  "customer": "<from Context if present or null>",
  "role": "<from Context if present>",
  "platform_hint": "<from Context if present>",
  "vendor": "<from Context if present>",
  "config_intents": [ "...", "..." ],
  "expected_state": [
    {
      "signal": "isis" | "bgp" | "mpls" | "sr" | "l2vpn" | "evpn" | "ip" | "intf" | "...",
      "observation_goals": [ "...", "..." ],
      "suggested_show": [ "show ..." ]   // must match platform_hint syntax
    }
  ]
}

For show_cmds.ini, include:
{
  "hostname": "Operational-Checks: show_cmds.ini",
  "role": "validation-commands",
  "checks": [
    { "intent": "...", "command": "show ...", "protocol": "..." }
  ]
}

Here is .txt example:
{
  "hostname": "A-PE-1",
  "provider": "Alpha",
  "customer": null,
  "role": "Provider-Edge",
  "platform_hint": "cisco-ios-xr",                 
  "config_intents": [
    "Enable BGP with IPv4 labeled-unicast for core reachability",
    "Assign SRGB/SRLB label blocks for Segment Routing",
    "Advertise Loopback0 /32 via BGP with label"
  ],
  "expected_state": [
    {
      "signal": "bgp",
      "observation_goals": [
        "BGP process is running",
        "Peers to core neighbors should be Established",
        "AFI/SAFI ipv4 labeled-unicast active",
        "Router-ID is set"
      ],
      "suggested_show": [
        "show bgp summary",
        "show bgp ipv4 labeled-unicast summary",
        "show running | section ^router bgp"
      ]
    },
    {
      "signal": "sr",
      "observation_goals": [
        "SRGB/SRLB present",
        "Prefix-SID attached to Loopback0"
      ],
      "suggested_show": [
        "show mpls lsd",
        "show mpls label table detail | inc SRGB|SRLB",
        "show run | section segment-routing"
      ]
    }
  ]
}

Here is show_cmds.ini example:
{
  "hostname": "Operational-Checks: show_cmds.ini",
  "role": "validation-commands",
  "checks": [
    {"intent": "Show ISIS config", "command": "show run router isis", "protocol": "ISIS"},
    {"intent": "ISIS neighbors",   "command": "show isis neighbors",  "protocol": "ISIS"}
  ]
}
"""

# —————————————————————————————————————————————————————————
# Few‑shot example to teach format
# —————————————————————————————————————————————————————————
FEW_SHOT = [
    # ---------- Example for a .txt config (BGP + SR, XR-ish) ----------
    {
        "role": "user",
        "content": """### Task: task-42.example
### A-PE-1.txt
segment-routing
 global-block 16000 23999
 local-block 25000 26000
!
route-policy SID($SID)
 set label-index $SID
end-policy
!
router bgp 100
 bgp router-id 1.0.101.1
 address-family ipv4 unicast
  network 1.0.101.1/32 route-policy SID(1)
  allocate-label all
 !
 neighbor-group TO_P
  remote-as 100
  update-source Loopback0
  address-family ipv4 labeled-unicast
 !
 neighbor 1.0.101.5
  use neighbor-group TO_P
 !
 neighbor 1.0.101.6
  use neighbor-group TO_P
"""
    },
    {
        "role": "assistant",
        "content": """{
        "hostname": "A-PE-1",
        "provider": "Alpha",
        "customer": null,
        "role": "Provider-Edge",
        "platform_hint": "cisco-ios-xr",
        "vendor": "cisco",
        "config_intents": [
          "Enable Segment Routing with SRGB/SRLB label blocks",
          "Run BGP AS 100 with IPv4 labeled-unicast for core reachability",
          "Use Loopback0 as update-source for core neighbors"
          "Advertise 1.0.101.1/32 with label via route-policy"
        ],
        "expected_state": [
          {
            "signal": "bgp",
            "observation_goals": [
              "BGP process is running",
              "Core neighbors should be Established",
              "AFI/SAFI ipv4 labeled-unicast active",
              "Router-ID set"
            ],
            "suggested_show": [
              { "cmd": "show bgp summary", "provenance": "llm", "confidence": "high", "platform": "cisco-ios-xr" },
              { "cmd": "show bgp ipv4 labeled-unicast summary", "provenance": "llm", "confidence": "med", "platform": "cisco-ios-xr" }
            ],
            "candidate_show": [
              { "cmd": "show run | section ^router bgp", "provenance": "llm", "confidence": "low", "platform": "cisco-ios-xr", "note": "IOS-style pipe may not work on XR" }
            ]
          },
          {
            "signal": "sr",
            "observation_goals": [
              "SRGB and SRLB present",
              "Prefix-SID bound to Loopback0"
            ],
            "suggested_show": [
              { "cmd": "show mpls lsd", "provenance": "llm", "confidence": "high", "platform": "cisco-ios-xr" }
            ],
            "candidate_show": [
              { "cmd": "show mpls label table detail | inc SRGB|SRLB", "provenance": "llm", "confidence": "med", "platform": "cisco-ios-xr", "note": "grep/pipes may vary" }
            ]
          }
  ]
}"""
    },

    # ---------- Example for show_cmds.ini (unchanged behavior) ----------
    {
        "role": "user",
        "content": """### Task: task-42.example
### show_cmds.ini
show run router isis
show isis neighbors
show ip route isis
"""
    },
    {
        "role": "assistant",
        "content": """{
  "hostname": "Operational-Checks: show_cmds.ini",
  "role": "validation-commands",
  "checks": [
    {"intent": "Show ISIS config", "command": "show running-config router isis", "protocol": "ISIS"},
    {"intent": "ISIS neighbors",   "command": "show isis neighbors",  "protocol": "ISIS"},
    {"intent": "IPv4 routes via ISIS", "command": "show ip route isis", "protocol": "ISIS"}
  ]
}"""
    }
]


def dbg(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [DEBUG agent_a] {msg}", flush=True)

def summarize_changes(changes):
    """
    Call the LLM once per config file and return full task summary as a JSON array string.
    Also harvest suggested/candidate show commands into a small local memory:
      - Global per-platform lexicon: /app/doo/_agent_knowledge/lexicon/<platform>.txt
      - Per-task observed (from show_cmds.ini): /app/doo/_agent_knowledge/observed/<config_dir>/<task>/commands.txt
    """
    base_dir = os.getenv("REPO_CLONE_DIR", "/opt/tasks").strip()
    first_path = changes[0][1]
    parts = first_path.split("/", 3)
    # parts = ['doo', 'configs.5', 'task-1', '...']
    config_dir = parts[1]
    task_name  = parts[2]
    task_dir   = os.path.join(base_dir, parts[0], parts[1], parts[2])

    dbg(f"task_dir: {task_dir}")
    summaries = []

    # For local memory aggregation
    per_platform_suggested: dict[str, set[str]] = {}  # platform -> cmds
    per_platform_candidate: dict[str, set[str]] = {}  # platform -> cmds
    per_task_observed_ini: set[str] = set()

    # ----------------------------
    # Process all .txt files in task folder
    # ----------------------------

    txt_files = sorted(glob.glob(os.path.join(task_dir, "*.txt")))
    dbg(f"txt_files found: {txt_files}")

    for txt in txt_files:
        base = os.path.basename(txt)
        if base.startswith("."):
            dbg(f"skip dotfile (txt): {txt}")
            continue

        rel = os.path.relpath(txt, base_dir)
        dbg(f"Including .txt: {rel}")    

        try:
            basename = os.path.basename(txt)
            content = open(txt, "r", encoding="utf-8").read()

            context = build_filename_context(basename)
            user_prompt = (
                f"### Task: {task_name}\n"
                f"### File: {basename}\n"
                f"### Context (DO NOT OVERRIDE)\n"
                f"```json\n{json.dumps(context, indent=2)}\n```\n\n"
                f"### Content\n"
                f"```text\n{content}\n```\n\n"
                f"Please respond with only valid JSON as specified."
            )
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + FEW_SHOT + [{"role": "user", "content": user_prompt}]
            response = call_llm(messages, temperature=0.0)
            summaries.append(response.strip())

            # ---- NEW: harvest shows from the JSON for lexicon ----
            try:
                obj = json.loads(response)
                plat = (obj.get("platform_hint") or "").strip() or "unknown"
                if isinstance(obj.get("expected_state"), list):
                    for est in obj["expected_state"]:
                        # suggested_show can be list[str] or list[dict{"cmd":..., "confidence":..., "platform":...}]
                        for bucket_name, store in (("suggested_show", per_platform_suggested),
                                                   ("candidate_show", per_platform_candidate)):
                            cmds = est.get(bucket_name) or []
                            for item in cmds:
                                if isinstance(item, dict):
                                    cmd = item.get("cmd", "").strip()
                                    # Only store if platform matches the file’s platform_hint (avoid cross-pollination)
                                    p_ok = (item.get("platform") or plat) == plat
                                    if cmd and p_ok:
                                        store.setdefault(plat, set()).add(cmd)
                                else:
                                    # plain string fallback
                                    cmd = str(item).strip()
                                    if cmd:
                                        store.setdefault(plat, set()).add(cmd)
            except Exception as e:
                dbg(f"harvest(JSON) failed for {basename}: {e}")

        except Exception as e:
            dbg(f"error reading {txt}: {e}")


    # ----------------------------
    # Process changed .ini files (e.g. show_cmds.ini) → per-task observed
    # ----------------------------
    for sha, path in changes:
        if not path.endswith(".txt"):
            full = os.path.join(base_dir, path)
            basename = os.path.basename(path)
            dbg(f"Including non-.txt: {path}")

            # Only process show_cmds.ini; skip all other artifacts (.DS_Store/.md/.json/etc.)
            if basename.startswith("."):
                dbg(f"skip dotfile: {path}")
                continue
            if basename != "show_cmds.ini":
                dbg(f"skip non-ini artifact: {path}")
                continue

            try:
                content = open(full, "r", encoding="utf-8").read()
                context = {
                    "hostname": "Operational-Checks: show_cmds.ini",
                    "provider": None,
                    "customer": None,
                    "role": "validation-commands",
                    "platform_hint": None,
                    "vendor": "cisco"
                }
                user_prompt = (
                    f"### Task: {task_name}\n"
                    f"### File: {basename}\n"
                    f"### Context\n"
                    f"```json\n{json.dumps(context, indent=2)}\n```\n\n"
                    f"### Content\n"
                    f"```ini\n{content}\n```\n\n"
                    f"Please respond with only valid JSON as specified."
                )
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *FEW_SHOT,
                    {"role": "user", "content": user_prompt}
                ]
                response = call_llm(messages, temperature=0.0)
                summaries.append(response.strip())

                # Harvest observed "show ..." lines from the INI itself
                try:
                    ini_cmds = _extract_show_cmds_from_ini(content)
                    per_task_observed_ini.update(ini_cmds)
                except Exception as e:
                    dbg(f"harvest(INI) failed for {basename}: {e}")

            except Exception as e:
                dbg(f"error reading {full}: {e}")

    for sha, path in changes:
      if not path.endswith(".txt"):
          full = os.path.join(base_dir, path)
          basename = os.path.basename(path)
          dbg(f"Including non-.txt: {path}")

          # Only process show_cmds.ini; skip all other artifacts (.DS_Store/.md/.json/etc.)
          if basename.startswith("."):
              dbg(f"skip dotfile: {path}")
              continue
          if basename != "show_cmds.ini":
              dbg(f"skip non-ini artifact: {path}")
              continue

          try:
              content = open(full, "r", encoding="utf-8").read()
              context = {
                  "hostname": "Operational-Checks: show_cmds.ini",
                  "provider": None,
                  "customer": None,
                  "role": "validation-commands",
                  "platform_hint": None,
                  "vendor": "cisco"
              }
              user_prompt = (
                  f"### Task: {task_name}\n"
                  f"### File: {basename}\n"
                  f"### Context\n"
                  f"```json\n{json.dumps(context, indent=2)}\n```\n\n"
                  f"### Content\n"
                  f"```ini\n{content}\n```\n\n"
                  f"Please respond with only valid JSON as specified."
              )
              messages = [
                  {"role": "system", "content": SYSTEM_PROMPT},
                  *FEW_SHOT,
                  {"role": "user", "content": user_prompt}
              ]
              response = call_llm(messages, temperature=0.0)
              summaries.append(response.strip())

              # Harvest observed "show ..." lines from the INI itself
              try:
                  ini_cmds = _extract_show_cmds_from_ini(content)
                  per_task_observed_ini.update(ini_cmds)
              except Exception as e:
                  dbg(f"harvest(INI) failed for {basename}: {e}")

          except Exception as e:
              dbg(f"error reading {full}: {e}")
            

    # ----------------------------
    # Persist local memories (lexicon & observed)
    # ----------------------------
    try:
        # RULE: All LLM-proposed shows (suggested or candidate) go to _candidates ONLY.
        #       Trusted lexicon is reserved for OBSERVED sources (ini/md), which we persist separately below.

        # XR guard: demote IOS-style pipes (| section) for XR into _candidates (kept here for clarity).
        def _demote_for_platform(plat: str, cmd: str) -> bool:
            if plat == "cisco-ios-xr" and "| section" in cmd.lower():
                return True
            return False

        # 1) Write suggested → _candidates
        for plat, cmds in per_platform_suggested.items():
            cand_path = os.path.join(LEXICON_ROOT, "_candidates", f"{plat}.txt")
            clean = []
            for c in sorted(cmds):
                if _demote_for_platform(plat, c):
                    dbg(f"[lexicon] XR guard (suggested): demoted IOS-style pipe → candidates: {c}")
                clean.append(c)
            _append_unique_lines(cand_path, clean)
            dbg(f"[lexicon] appended {len(clean)} suggested (LLM) → {cand_path}")

        # 2) Write candidates → _candidates (as-is)
        for plat, cmds in per_platform_candidate.items():
            cand_path = os.path.join(LEXICON_ROOT, "_candidates", f"{plat}.txt")
            _append_unique_lines(cand_path, sorted(cmds))
            dbg(f"[lexicon] appended {len(cmds)} candidates (LLM) → {cand_path}")

        # 3) Per-task OBSERVED from show_cmds.ini → trusted observed store
        if per_task_observed_ini:
            observed_path = os.path.join(OBSERVED_ROOT, config_dir, task_name, "commands.txt")
            _append_unique_lines(observed_path, sorted(per_task_observed_ini))
            dbg(f"[observed] appended {len(per_task_observed_ini)} shows → {observed_path}")

    except Exception as e:
        dbg(f"[memory] persist failed: {e}")
        


    # ----------------------------
    if not summaries:
        dbg("No summaries returned from LLM.")
        return "[]"

    # Optional cleanup: ensure trusted lexicon only contains observed items
    try:
        sanitize_lexicon(AGENT_KNOWLEDGE_ROOT)
    except Exception as e:
        dbg(f"[lexicon] sanitize failed: {e}")

    return "[\n" + ",\n".join(summaries) + "\n]"
