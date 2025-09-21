# agents/agent-8/triage_llm.py
# This file is responsible for asking the LLM to analyze
# the output of one or more show commands during triage.
# It builds a clear prompt, calls the LLM, and parses
# the JSON reply into a simple Python dict.

import json
from typing import List, Dict
from datetime import datetime

# helper function call_llm(prompt: str) -> str 
try:
    from shared.llm_api import call_llm  # type: ignore
except Exception:
    call_llm = None  # degrade gracefully

LLM_TEMPERATURE = float(os.getenv("A8_LLM_TEMPERATURE", "0.1"))

# A focused system prompt to keep replies concise and JSON-only
SYSTEM_PROMPT = (
    "You are a senior network troubleshooting assistant. "
    "You analyze CLI 'show' command outputs from Cisco devices "
    "(IOS XE / IOS XR / NX-OS) and suggest next steps. "
    "Always return STRICT JSON only (no prose, no markdown, no backticks). "
    "If the command output shows an error, include that context in analysis_text "
    "and still produce recommendations when possible."
)

def build_prompt(host: str, cmds: List[str], outputs: List[str],
                 history: List[Dict]) -> str:
    """
    Build the text prompt for the LLM.

    Includes:
    - Host name
    - Commands just run + their outputs
    - Recent triage history (for context)
    """
    prompt = []
    prompt.append(f"You are analyzing device: {host}")
    prompt.append("Here are the command outputs:")

    for cmd, out in zip(cmds, outputs):
        prompt.append(f"\nCOMMAND: {cmd}\nOUTPUT:\n{out}\n")

    if history:
        prompt.append("\nRecent triage history:")
        for step in history[-3:]:  # include last 3 steps
            prompt.append(f"- {step.get('commands', [])}: {step.get('analysis','')}")

    prompt.append(
        """
Return JSON only with this format:
{
  "analysis_text": "<short plain analysis of outputs>",
  "direction": "<guidance for next steps>",
  "recommended": [
    {"command": "<cmd1>", "tech": "<bucket like bgp/ospf/interfaces>", "trust_hint": "low"},
    {"command": "<cmd2>", "tech": "interfaces", "trust_hint": "low"}
  ],
  "execution_judgment": {
    "<cmd1>": "ok" | "partial" | "error"
  }
}
"""
    )
    return "\n".join(prompt)


def call_llm_json(prompt: str) -> Dict:
    """
    Call the LLM and parse its JSON output safely.
    Returns a dict, or empty structure if parsing fails.
    """
    try:
        if call_llm is None:
            raise RuntimeError("LLM API not available")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        raw = call_llm(messages, temperature=LLM_TEMPERATURE)
        return json.loads(raw)
    except Exception as e:
        # fallback: return empty structure
        return {
            "analysis_text": f"LLM call failed: {e}",
            "direction": "",
            "recommended": [],
            "execution_judgment": {}
        }


def triage_llm_analyze(host: str, cmds: List[str], outputs: List[str],
                       history: List[Dict]) -> Dict:
    """
    Main entrypoint: build prompt, call LLM, return analysis dict.
    """
    prompt = build_prompt(host, cmds, outputs, history)
    result = call_llm_json(prompt)

    # Always ensure required keys exist
    return {
        "analysis_text": result.get("analysis_text", ""),
        "direction": result.get("direction", ""),
        "recommended": result.get("recommended", []),
        "execution_judgment": result.get("execution_judgment", {})
    }