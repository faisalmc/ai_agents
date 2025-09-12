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

from llm_clients.llm_api import call_llm

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
# —————————————————————————————————————————————————————————
# Updated system prompt for individual file processing
# —————————————————————————————————————————————————————————
SYSTEM_PROMPT = """\
You are a Cisco Service Provider / Customer-Edge configuration assistant.
You will be given a Task name and a single file (configuration .txt OR operational checks .ini).

IMPORTANT:
• A small JSON "Context" may be provided. If present, you MUST copy its fields verbatim
  into your output (do not re-infer or override). These keys may include:
  {"hostname","provider","customer","role","platform_hint","vendor"}.
• When suggesting any show commands, you MUST align to platform_hint:
  - platform_hint == "cisco-ios"     → IOS-style CLI (e.g., 'show run | section ...', 'show ip ...')
  - platform_hint == "cisco-ios-xr"  → IOS-XR CLI (e.g., 'show running-config router ...', 'show route ...')
• Never mix platforms in suggested commands.

Your job is to emit ONE JSON object per file with:
- core identity (hostname, role, provider/customer),
- concise "config_intents" (natural language),
- and a LIGHTWEIGHT, FLEXIBLE "expected_state" that Agent-5 can use as evidence targets.
Keep the schema loose enough to cover new vendors/protocols without breaking.

Rules

A. For .txt files (device configs):
   • Hostname = filename without extension (e.g. “A-PE-1.txt” → “A-PE-1”).
   • Decode X-ROLE-N:
     - If ROLE in {PE, P, ASBR, RR}, then X = SP (A=Alpha, B=Beta, C=Charlie).
     - If ROLE == CE, then X = Customer (B=Blue, S=Silver, R=Red, M=Magneto).
   • Extract the *design intent* behind the configuration (not just CLI lines).
   • Group related lines into meaningful intents using declarative language.
   • Include a lightweight “expected_state” section per major signal (e.g., isis, bgp, mpls):
     - signal: <string>
     - observation_goals: [list of checks in human terms]
     - suggested_show: [IOS or IOS-XR commands that match platform_hint]
  • Build a flexible "expected_state" array: each element is an observation target the NOC should later verify.
    This is NOT strict and must tolerate unknowns. Use free-form text where exact values are not present.
    Example elements:
      {
        "signal": "bgp",                        // e.g. bgp, isis, ospf, mpls, evpn, l2vpn, sr, srv6, intf, ip, ntp, aaa, qos, aaa, telemetry, ...
        "observation_goals": [
          "BGP process running",
          "EBGP peers to core neighbors should be Established",
          "AFI/SAFI ipv4 labeled-unicast active",
          "Router-ID present"
        ],
        "suggested_show": [
          "show bgp summary",
          "show bgp ipv4 labeled-unicast summary",
          "show running | section ^router bgp"
        ],
        "notes": "Do not assume peer IPs if not in config. Use platform-neutral verbs."
      }
    • Keep 2–6 targets max. Prefer signals you truly see in config (bgp/isis/mpls/sr/evpn/etc.). It’s OK if some are high-level.

B. For show_cmds.ini:
   • This file contains commands for operational checks after configuration is applied.
   • Hostname = "Operational-Checks: show_cmds.ini"
   • Role = "validation-commands"
   • Each line is a "show" command.
   • Group them by protocol (e.g. ISIS, BGP, MPLS, SR, OSPF, etc.) if possible.
   • Each entry must include:
     - intent (in human terms)
     - command (the exact CLI line)
     - protocol (category like ISIS, BGP, etc.)

Output:
Respond ONLY with valid JSON (ONE object). Do not add commentary outside JSON.

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
          "Advertise Loopback0 /32 with label via route-policy"
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
              "show bgp summary",
              "show bgp neighbors brief",
              "show bgp ipv4 labeled-unicast summary",
              "show running-config router bgp"
            ]
          },
          {
            "signal": "sr",
            "observation_goals": [
              "SRGB and SRLB present",
              "Prefix-SID bound to Loopback0"
            ],
            "suggested_show": [
              "show mpls lsd forwarding",
              "show mpls label table detail | inc "SRGB|SRLB"",
              "show running-config segment-routing"
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
    """
    base_dir = os.getenv("REPO_CLONE_DIR", "/opt/tasks").strip()
    first_path = changes[0][1]
    parts = first_path.split("/", 3)
    task_name = parts[2]
    task_dir = os.path.join(base_dir, parts[0], parts[1], parts[2])

    dbg(f"task_dir: {task_dir}")
    summaries = []

    # Process all .txt files in task folder
    txt_files = sorted(glob.glob(os.path.join(task_dir, "*.txt")))
    dbg(f"txt_files found: {txt_files}")

    for txt in txt_files:
      rel = os.path.relpath(txt, base_dir)
      dbg(f"Including .txt: {rel}")
      try:
          basename = os.path.basename(txt)
          context = build_filename_context(basename)
          content = open(txt, "r", encoding="utf-8").read()   # ← ADD THIS
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
      except Exception as e:
          dbg(f"error reading {txt}: {e}")

    # # Process changed .ini files (e.g. show_cmds.ini)
    # for sha, path in changes:
    #     if not path.endswith(".txt"):
    #         full = os.path.join(base_dir, path)
    #         dbg(f"Including non-.txt: {path}")
    #         try:
    #             content = open(full).read() if os.path.exists(full) else "<missing>"
    #             user_prompt = f"### Task: {task_name}\n\n### {os.path.basename(path)}\n```ini\n{content}\n```\n\nPlease respond with only valid JSON as specified."
    #             messages = [{"role": "system", "content": SYSTEM_PROMPT}] + FEW_SHOT + [{"role": "user", "content": user_prompt}]
    #             response = call_llm(messages, temperature=0.0)
    #             summaries.append(response.strip())
    #         except Exception as e:
    #             dbg(f"error reading {full}: {e}")

    # Process changed .ini files (e.g. show_cmds.ini)

    for sha, path in changes:
        if not path.endswith(".txt"):
            full = os.path.join(base_dir, path)
            dbg(f"Including non-.txt: {path}")
            try:
                basename = os.path.basename(path)
                content = open(full, "r", encoding="utf-8").read()   # ← ADD THIS
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
            except Exception as e:
                dbg(f"error reading {full}: {e}")

    if not summaries:
        dbg("No summaries returned from LLM.")
        return "[]"

    return "[\n" + ",\n".join(summaries) + "\n]"
