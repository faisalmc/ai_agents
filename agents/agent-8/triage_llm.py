# agents/agent-8/triage_llm.py
# This file is responsible for asking the LLM to analyze
# the output of one or more show commands during triage.
# It builds a clear prompt, calls the LLM, and parses
# the JSON reply into a simple Python dict.

import json, os
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
    - Commands just run + their outputs (the current request always has 1)
    - Recent triage history (for context)
    - STRICT rules to avoid config-mode suggestions or unrelated analysis
    """
    prompt = []
    prompt.append(f"You are analyzing network device: {host}.")
    prompt.append("You are given fresh CLI outputs below. Base your analysis ONLY on these outputs.")
    prompt.append("Do NOT reuse conclusions from prior steps unless they are consistent with the outputs in this message.")
    prompt.append("Recommend ONLY read-only 'show' commands. Never recommend configuration mode commands.")
    prompt.append("If you believe configuration is needed, instead recommend a 'show' command that would validate the hypothesis.")
    prompt.append("If the output indicates an error (e.g., '% Invalid input', 'Unknown command'), your analysis_text should say so and execution_judgment must be 'error' for that command.")
    prompt.append("Be concise and practical.")

    prompt.append("\nHere are the command outputs:")
    for cmd, out in zip(cmds, outputs):
        prompt.append(f"\nCOMMAND: {cmd}\nOUTPUT:\n{out}\n")

    if history:
        prompt.append("\nRecent triage history (last 3 steps, for context only):")
        for step in history[-3:]:
            prompt.append(f"- ran: {step.get('commands', [])} → {step.get('analysis','')}")

    prompt.append(
        """
Return JSON only with this exact shape:
{
  "analysis_text": "<short plain analysis derived strictly from the outputs above>",
  "direction": "<next diagnostic steps in plain English; no config>",
  "recommended": [
    {"command": "<read-only show cmd 1>", "tech": "bgp|interfaces|ospf|routing|misc", "trust_hint": "low"},
    {"command": "<read-only show cmd 2>", "tech": "interfaces", "trust_hint": "low"}
  ],
  "execution_judgment": {
    "<the command you just analyzed>": "ok" | "partial" | "error"
  }
}
- The 'recommended' list MUST contain only read-only 'show' commands.
- If the output indicates an invalid or failed command, set execution_judgment to "error".
- Do not invent facts not present in the outputs.
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
        # --- log raw exchange ---
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = pathlib.Path(debug_dir) / f"llm_debug_{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "messages": messages,
                "raw": raw
            }, f, indent=2)

        return json.loads(raw)

    except Exception as e:
        # --- also log failures ---
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = pathlib.Path(debug_dir) / f"llm_debug_error_{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "error": str(e),
                "prompt": prompt
            }, f, indent=2)

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