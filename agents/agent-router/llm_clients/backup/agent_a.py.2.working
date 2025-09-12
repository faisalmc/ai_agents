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
from datetime import datetime

from llm_clients.llm_api import call_llm

# —————————————————————————————————————————————————————————
# Updated system prompt for individual file processing
# —————————————————————————————————————————————————————————
SYSTEM_PROMPT = """\
You are a Cisco SP / Customer‑Edge configuration assistant.
You will be given a Task name and a single file (configuration or operational check).

Rules:

1. For .txt files:
   • Hostname = filename without extension (e.g. “A-PE-1.txt” → “A-PE-1”).
   • Decode X-ROLE-N:
     - If ROLE in {PE, P, ASBR, RR}, then X = SP (A=Alpha, B=Beta, C=Charlie).
     - If ROLE == CE, then X = Customer (B=Blue, S=Silver, R=Red, M=Magneto).
   • Extract the *design intent* behind the configuration (not just CLI lines).
   • Group related lines into meaningful intents.
   • Use declarative language (e.g. “Enable BGP peering with CE”).

2. For show_cmds.ini:
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
Respond ONLY with valid JSON (one object), like:
{
  "hostname": "Operational-Checks",
  "role": "Validation-Script",
  "checks": [
    {
      "intent": "Verify BGP neighbor status",
      "command": "show bgp ipv4 unicast summary",
      "protocol": "BGP"
    },
    {
      "intent": "Check ISIS IPv4 routing table",
      "command": "show isis ipv4 route",
      "protocol": "ISIS"
    }
  ]
}
"""

# —————————————————————————————————————————————————————————
# Few‑shot example to teach format
# —————————————————————————————————————————————————————————
FEW_SHOT = [
    # Example for .txt config
    {
        "role": "user",
        "content": """### Task: task-17.example
### A-PE-1.txt
interface GigabitEthernet0/0
no shutdown
ip address 10.13.1.1/30
ipv6 address 2620:fc7:13:1::1/64
"""
    },
    {
        "role": "assistant",
        "content": """{
  "hostname": "A-PE-1",
  "provider": "Alpha",
  "customer": null,
  "role": "Provider-Edge",
  "config_intents": [
    "Enable interface GigabitEthernet0/0 with IPv4 10.13.1.1/30",
    "Enable interface GigabitEthernet0/0 with IPv6 2620:fc7:13:1::1/64"
  ]
}"""
    },

    # Example for show_cmds.ini
    {
        "role": "user",
        "content": """### Task: task-17.example
### show_cmds.ini
show run router isis
show route ipv4 isis
"""
    },
    {
        "role": "assistant",
        "content": """{
  "hostname": "Operational-Checks: show_cmds.ini",
  "role": "validation-commands",
  "checks": [
    {
      "intent": "Show ISIS configuration",
      "command": "show run router isis",
      "protocol": "ISIS"
    },
    {
      "intent": "Display IPv4 routes learned via ISIS",
      "command": "show route ipv4 isis",
      "protocol": "ISIS"
    }
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
            content = open(txt).read()
            user_prompt = f"### Task: {task_name}\n\n### {os.path.basename(txt)}\n```text\n{content}\n```\n\nPlease respond with only valid JSON as specified."
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
                content = open(full).read() if os.path.exists(full) else "<missing>"
                user_prompt = f"### Task: {task_name}\n\n### {os.path.basename(path)}\n```ini\n{content}\n```\n\nPlease respond with only valid JSON as specified."
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
