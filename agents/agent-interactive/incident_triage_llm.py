"""
agents/agent-interactive/incident_triage_llm.py
------------------------------------------------
Phase-2 adaptation of Agent-8's triage_llm.py.

Purpose:
- Automatically analyze normalized incident JSON (Phase-1 output)
- Generate diagnostic "show" command recommendations using the LLM
- Optionally classify missing 'tech' fields using incident_commands_trusted.choose_tech()
- Keep logs and debug output isolated under: /app/shared/_incident_knowledge

Key differences from Agent-8 version:
- No user free-text prompt (auto input from normalized JSON)
- Vendor/platform/context extracted from structured JSON
- Uses incident_commands_trusted.py helpers instead of agent-8 equivalents
"""

import os
import json
import pathlib
from datetime import datetime, timezone
from typing import Dict, List

# --------------------------------------------------------------------
# Step 1: Import helpers and setup environment
# --------------------------------------------------------------------
try:
    from shared.llm_api import call_llm  # main LLM interface
except Exception:
    call_llm = None  # fallback if unavailable

# Reuse classification helpers for tech buckets
import incident_commands_trusted  

# Dedicated debug folder for this agent
DEBUG_DIR = "/app/shared/_incident_knowledge/llm_debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

LLM_TEMPERATURE = float(os.getenv("AINT_LLM_TEMPERATURE", "0.1"))

# --------------------------------------------------------------------
# Step 2: Define the system role for the LLM
# --------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a senior network troubleshooting assistant. "
    "You analyze structured incident information and propose relevant "
    "read-only diagnostic 'show' commands for Cisco devices "
    "(IOS XE / IOS XR / NX-OS). "
    "Always return STRICT JSON only — no explanations, markdown, or prose. "
    "If the command output shows an error (e.g., '% Invalid input', 'Unknown command'), "
    "include that context in analysis_text and still produce recommendations when possible."
)


# --------------------------------------------------------------------
# Step 3: Build prompt automatically from normalized JSON
# --------------------------------------------------------------------
def build_incident_prompt(normalized: Dict) -> str:
    """
    Build a structured prompt for the LLM using Phase-1 normalized JSON.

    Expected normalized shape (per phase1_ingest.compose_final_ies):
    {
      "incident_id": "...",
      "source":   {"hostname": "...", "ip": "...", "vendor": "...", "platform": "..."},
      "context":  {"severity": "...", "timestamp": "...", "event_class": "..."},
      "symptom_text": "...",
      "family": { ... },   # agent-specific family block (e.g., interface/type/status/flags)
      "confidence": 0.9
    }
    """
    # ---- Step 1: Safe extraction from normalized IES ----
    source   = (normalized.get("source")  or {})
    context  = (normalized.get("context") or {})
    family   = (normalized.get("family")  or {})

    vendor      = (source.get("vendor")   or "unknown")
    platform    = (source.get("platform") or "unknown")
    hostname    = (source.get("hostname") or "unknown")
    ip_addr     = (source.get("ip")       or "unknown")

    severity    = (context.get("severity")    or "unknown")
    ts_iso      = (context.get("timestamp")   or "unknown")
    event_class = (context.get("event_class") or "unknown")

    symptom     = (normalized.get("symptom_text") or "").strip()
    confidence  = normalized.get("confidence")

    # Render family block as a compact JSON fragment for context (safe/short)
    try:
        family_snippet = json.dumps(family, separators=(",", ":"), ensure_ascii=False)
    except Exception:
        family_snippet = "{}"

    # Allowed tech buckets (dynamic, single source of truth)
    tech_list = ", ".join(incident_commands_trusted.TECH_BUCKETS)

    # ---- Step 2: Compose prompt lines ----
    prompt = []
    prompt.append("You are analyzing an automatically detected network incident.")
    prompt.append(f"Vendor: {vendor}")
    prompt.append(f"Platform: {platform}")
    prompt.append(f"Hostname: {hostname}")
    prompt.append(f"IP: {ip_addr}")
    prompt.append(f"Severity: {severity}")
    prompt.append(f"Event class: {event_class}")
    prompt.append(f"Timestamp (UTC): {ts_iso}")
    if confidence is not None:
        prompt.append(f"Detector confidence: {confidence}")
    prompt.append(f"Family block (context): {family_snippet}")
    prompt.append("")
    prompt.append("Detected symptom:")
    prompt.append(f"\"{symptom}\"")
    prompt.append("")
    prompt.append("Your task:")
    prompt.append("- Propose 2–5 relevant *read-only* 'show' commands to begin diagnosis.")
    prompt.append("- Prefer commands valid for the given vendor/platform.")
    prompt.append("- Each recommendation MUST include:")
    prompt.append('    - "command": the exact CLI string')
    prompt.append(f'    - "tech": one of [{tech_list}]')
    prompt.append('    - "trust_hint": always "low"')
    prompt.append("")
    prompt.append("- Respond only with verifiable, factual recommendations derived from the data above.")
    prompt.append("- If uncertain or insufficient context is available, reply with an empty 'recommended' list instead of guessing.")
    prompt.append("Return STRICT JSON only:")
    prompt.append("{")
    prompt.append('  "recommended": [')
    prompt.append('    {"command": "<cmd>", "tech": "<one-of-allowed>", "trust_hint": "low"}')
    prompt.append("  ]")
    prompt.append("}")
    return "\n".join(prompt)


# --------------------------------------------------------------------
# Step 4: LLM JSON-safe call helper
# --------------------------------------------------------------------
def call_llm_json(prompt: str) -> Dict:
    """
    Call the LLM API safely and parse JSON response.
    Logs both success and failure cases for debug review.
    """
    try:
        if call_llm is None:
            raise RuntimeError("LLM API not available")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        raw = call_llm(messages, temperature=LLM_TEMPERATURE)

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        debug_path = pathlib.Path(DEBUG_DIR) / f"llm_debug_{ts}.json"
        with open(debug_path, "w", encoding="utf-8") as f:
            json.dump({"messages": messages, "raw": raw}, f, indent=2)

        return json.loads(raw)
    except Exception as e:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        err_path = pathlib.Path(DEBUG_DIR) / f"llm_debug_error_{ts}.json"
        with open(err_path, "w", encoding="utf-8") as f:
            json.dump({"error": str(e), "prompt": prompt[:1000]}, f, indent=2)
        return {"recommended": [], "error": str(e)}

# --------------------------------------------------------------------
# Step 5: Propose diagnostic commands (main entrypoint)
# --------------------------------------------------------------------
def incident_llm_propose(normalized: Dict) -> Dict:
    """
    Generate LLM-based diagnostic command suggestions from structured incident data.
    - No user free-text input in Phase-2
    - We still normalize/fix missing tech via choose_tech()
    """
    if not isinstance(normalized, dict):
        return {"recommended": [], "error": "Invalid normalized input"}

    # Step 1: Build prompt from normalized IES
    prompt = build_incident_prompt(normalized)
    print("\n[DEBUG:incident_llm_propose] Built prompt successfully", flush=True)
    print(f"[DEBUG] Prompt (first 400 chars): {prompt[:400]}...\n", flush=True)

    # Step 2: Call LLM and parse JSON
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] [DEBUG] Calling LLM for proposal...", flush=True)
    result = call_llm_json(prompt)
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] [DEBUG] LLM propose response keys: {list(result.keys())}", flush=True)

    # --- Extra debug for transparency ---
    try:
        print(f"[{datetime.now(timezone.utc).isoformat()}] [DEBUG] Full LLM response:\n{json.dumps(result, indent=2)[:1500]}...\n", flush=True)
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] [ERROR] Failed to print LLM response: {e}", flush=True)

    if not isinstance(result, dict):
        return {"recommended": [], "error": "Invalid LLM response format"}

    recs = result.get("recommended", []) or []

    # Step 3: Backup classification using choose_tech() when LLM tech is missing/invalid
    final_recs = []
    for rec in recs:
        cmd = (rec.get("command") or "").strip()
        hinted_tech = rec.get("tech")
        if not cmd:
            continue

        # Ensure 'tech' ∈ TECH_BUCKETS; otherwise classify from the command string.
        final_tech = incident_commands_trusted.choose_tech(cmd, hinted_tech)
        rec["tech"] = final_tech
        rec["trust_hint"] = rec.get("trust_hint", "low")
        final_recs.append(rec)

        print(f"[DEBUG:incident_llm_propose] Command={cmd}, hinted={hinted_tech}, final_tech={final_tech}", flush=True)


    # --- Step 4: Return structured response ---
    return {
        "analysis_text": f"Proposed diagnostic commands for: {normalized.get('symptom_text','')}",
        "direction": "Run these commands to begin root-cause isolation.",
        "recommended": final_recs
    }

# --------------------------------------------------------------------
# Step 6: Incident LLM Analyzer (same pattern as Agent-8)
# --------------------------------------------------------------------
def incident_llm_analyze(host: str, cmds: List[str], outputs: List[str], history: List[Dict]) -> Dict:
    """
    Analyze CLI outputs (read-only 'show' commands) for a given host and
    return structured LLM feedback. Mirrors Agent-8 behavior:

    - Strict JSON response
    - If output indicates an error ('% Invalid input', etc.), analysis_text must say so
      and execution_judgment must be "error" for that command.
    - Uses recent triage history (last few steps) only as context.
    """
    # ---- Step 1: Compose detailed analysis prompt (Agent-8 parity) ----
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

    tech_list = ", ".join(incident_commands_trusted.TECH_BUCKETS)
    prompt.append(
        f"""
Return JSON only with this exact shape:
{{
  "analysis_text": "<short plain analysis derived strictly from the outputs above>",
  "direction": "<next diagnostic steps in plain English; no config>",
  "recommended": [
    {{"command": "<read-only show cmd 1>", "tech": "<one-of: {tech_list}>", "trust_hint": "low"}},
    {{"command": "<read-only show cmd 2>", "tech": "<one-of: {tech_list}>", "trust_hint": "low"}}
  ],
  "execution_judgment": {{
    "<the command you just analyzed>": "ok" | "partial" | "error"
  }}
}}

The 'recommended' list MUST contain only read-only 'show' commands.
If the output indicates an invalid or failed command, set execution_judgment to "error".
Do not invent facts not present in the outputs.
"""
    )
    full_prompt = "\n".join(prompt)

    # ---- Step 2: Call LLM and return normalized structure ----
    result = call_llm_json(full_prompt)
    return {
        "analysis_text": result.get("analysis_text", ""),
        "direction": result.get("direction", ""),
        "recommended": result.get("recommended", []),
        "execution_judgment": result.get("execution_judgment", {})
    }
