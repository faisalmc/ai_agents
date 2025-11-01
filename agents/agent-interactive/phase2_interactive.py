"""
agents/agent-interactive/phase2_interactive.py
-----------------------------------------------
Phase-2 entrypoint for Incident-Agent (Agent-Interactive).

Purpose:
- Read Phase-1 normalized JSON from:
    agents/agent-interactive/incidents/<incident_id>/1-ingest/1-2.normalized.json
- Build context and run the LLM proposal step (incident_llm_propose) >> Step 4.2
- Classify proposed commands into trusted/untrusted using incident_commands_trusted >> Step 4.3
- (Later) dispatch trusted/untrusted commands to Agent-4 (capture layer) >> Step 4.4
- Call LLM analyzer (incident_llm_analyze) on captured outputs >> Step 4.5
- Write results into:    >> Step 4.
    agents/agent-interactive/incidents/<incident_id>/2-analyze/
        2.1-context.json
        2.2-runlog.jsonl
        2.3-evidence.json
- Append operational telemetry into logs/phase2_run_YYYYMMDD.jsonl. >> Step 4.8  
- Update triage history under /app/shared/_incident_knowledge/triage_history/ >> Step 4.7

No “promote” phase or /doo/ directories are used.
All persistent data (trusted commands, triage history, debug) lives under:
    /app/shared/_incident_knowledge/
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List

# --------------------------------------------------------------------
# Step 1: Import supporting Phase-2 modules
# --------------------------------------------------------------------
try:
    import incident_commands_trusted
    import incident_triage_llm
    import incident_triage_history
except Exception as e:
    raise ImportError(f"Failed to import Phase-2 incident_* modules: {e}")

import subprocess
from kafka import KafkaConsumer
import traceback
import time

# --------------------------------------------------------------------
# Step 2: Directories and constants
# --------------------------------------------------------------------
BASE_DIR = "/app/agents/agent-interactive"
INCIDENTS_DIR = os.path.join(BASE_DIR, "incidents")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


# --------------------------------------------------------------------
# Step 3: Utility helpers
# --------------------------------------------------------------------
def _load_normalized_json(path: str) -> Dict:
    """Read Phase-1 normalized JSON safely."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing normalized file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(data: Dict, path: str) -> None:
    """Write a JSON file (ensure parent folder)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _append_runlog(line: Dict) -> None:
    """Append one operational telemetry line to logs/phase2_run_YYYYMMDD.jsonl."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d")
    path = os.path.join(LOGS_DIR, f"phase2_run_{ts}.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line["ts"] = datetime.now(timezone.utc).isoformat()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")


# --------------------------------------------------------------------
# Step 4: Core orchestration
# --------------------------------------------------------------------
def run_phase2(incident_id: str) -> None:
    """
    Run full Phase-2 pipeline for a given incident.
    Reads 1-2.normalized.json, runs LLM propose/analyze, and writes outputs.
    """
    print(f"\n[INFO] === Running Phase-2 for incident {incident_id} ===", flush=True)

    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] [DEBUG] Phase-2 working directory: {os.getcwd()}", flush=True)
    print(f"[{ts}] [DEBUG] PYTHONPATH: {os.getenv('PYTHONPATH','<unset>')}", flush=True)

    # --- Step 4.1: Locate and load Phase-1 output ---
    norm_path = os.path.join(
        INCIDENTS_DIR, incident_id, "1-ingest", "1.2-normalized.json"
    )
    normalized = _load_normalized_json(norm_path)
    print(f"[DEBUG] Loaded normalized JSON from {norm_path}", flush=True)

    # --- Step 4.2: Run LLM propose ---
    proposal = incident_triage_llm.incident_llm_propose(normalized)
    context_out = os.path.join(INCIDENTS_DIR, incident_id, "2-analyze", "2.1-context.json")
    _save_json(proposal, context_out)
    print(f"[DEBUG] Wrote context output → {context_out}", flush=True)

    # --- Step 4.3: Split into trusted vs untrusted commands ---
    vendor = normalized.get("source", {}).get("vendor", "unknown")
    platform = normalized.get("source", {}).get("platform", "unknown")

    trusted_cmds, untrusted_cmds = [], []
    for rec in proposal.get("recommended", []):
        cmd = rec.get("command")
        if not cmd:
            continue
        if incident_commands_trusted.is_trusted(cmd, vendor, platform):
            trusted_cmds.append(cmd)
        else:
            untrusted_cmds.append(cmd)

    print(f"[INFO] Trusted cmds: {len(trusted_cmds)}, Untrusted cmds: {len(untrusted_cmds)}", flush=True)

    # # --- Step 4.4: Simulate Agent-4 capture (placeholder) ---
    # # For now, we assume outputs = empty placeholders until Agent-4 provides real captures.
    # outputs = [f"(Simulated output for: {c})" for c in trusted_cmds + untrusted_cmds]
    # all_cmds = trusted_cmds + untrusted_cmds


    # --- Step 4.4: Capture all commands (trusted + untrusted) ---
    plan_ini = os.path.join(INCIDENTS_DIR, incident_id, "2-analyze", "plan.ini")
    capture_dir = os.path.join(INCIDENTS_DIR, incident_id, "2-analyze", "2-capture")
    os.makedirs(capture_dir, exist_ok=True)

    all_cmds = trusted_cmds + untrusted_cmds
    if not all_cmds:
        print("[WARN] No commands to capture — skipping run_show_commands_interactive", flush=True)
        outputs = []
    else:
        # --- Build plan.ini with per-host sections (same style as Agent-4/8) ---
        host = normalized.get("source", {}).get("hostname", "unknown")
        with open(plan_ini, "w", encoding="utf-8") as ini:
            ini.write(f"[{host}]\n")
            for cmd in all_cmds:
                ini.write(f"{cmd}\n")
        print(f"[DEBUG] Wrote plan.ini → {plan_ini}", flush=True)

        # --- Run capture synchronously ---
        capture_script = "/app/agents/agent-interactive/run_show_commands_interactive.py"
        cmd = ["python3", capture_script, "--ini", plan_ini, "--out-dir", capture_dir]
        try:
            print(f"[INFO] Starting capture for {host} ({len(all_cmds)} cmds)", flush=True)
            subprocess.run(cmd, check=True)
            print(f"[INFO] Capture completed → {capture_dir}", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Capture script failed: {e}", flush=True)

        # --- Parse Markdown logs to collect outputs ---
        from shared.helpers import extract_cmd_output
        log_path = os.path.join(capture_dir, f"{host}.md")
        if not os.path.isfile(log_path):
            print(f"[ERROR] Missing capture log: {log_path}", flush=True)
            outputs = []
        else:
            body = open(log_path, encoding="utf-8").read()
            outputs = []
            for cmd in all_cmds:
                out = extract_cmd_output(body, cmd)
                outputs.append(out)

        # --- Promote successful untrusted commands ---
        ERROR_MARKERS = [
            "% Invalid input", "Unknown command",
            "Incomplete command", "Ambiguous command"
        ]
        promoted = []
        vendor = normalized.get("source", {}).get("vendor", "unknown")
        platform = normalized.get("source", {}).get("platform", "unknown")

        for cmd, out in zip(untrusted_cmds, outputs[-len(untrusted_cmds):] or []):
            if out and not any(m in out for m in ERROR_MARKERS):
                incident_commands_trusted.promote(cmd, vendor, platform, None)
                promoted.append(cmd)
        print(f"[INFO] Promoted {len(promoted)} new trusted commands", flush=True)


    # --- Step 4.5: Run analyzer step ---
    history = incident_triage_history.collect_recent_steps(incident_id)
    analysis = incident_triage_llm.incident_llm_analyze(
        normalized.get("source", {}).get("hostname", "unknown"),
        all_cmds,
        outputs,
        history,
    )

    evidence_out = os.path.join(INCIDENTS_DIR, incident_id, "2-analyze", "2.3-evidence.json")
    _save_json(analysis, evidence_out)
    print(f"[DEBUG] Wrote evidence output → {evidence_out}", flush=True)

    # --- Step 4.6: Write runlog (sequence of steps) ---
    step_record = {
        "incident_id": incident_id,
        "host": normalized.get("source", {}).get("hostname"),
        "commands": all_cmds,
        "trusted": trusted_cmds,
        "unvalidated": untrusted_cmds,
        "analysis": analysis.get("analysis_text", ""),
        "direction": analysis.get("direction", ""),
    }

    runlog_out = os.path.join(INCIDENTS_DIR, incident_id, "2-analyze", "2.2-runlog.jsonl")
    os.makedirs(os.path.dirname(runlog_out), exist_ok=True)
    with open(runlog_out, "a", encoding="utf-8") as f:
        f.write(json.dumps(step_record) + "\n")
    print(f"[DEBUG] Wrote runlog → {runlog_out}", flush=True)

    # --- Step 4.7: Append to global triage history ---
    incident_triage_history.append_step(
        incident_id=incident_id,
        host=normalized.get("source", {}).get("hostname", "unknown"),
        cmds=all_cmds,
        analysis=analysis.get("analysis_text", ""),
        direction=analysis.get("direction", ""),
        trusted=trusted_cmds,
        unvalidated=untrusted_cmds,
    )

    # --- Step 4.8: Append telemetry line ---
    _append_runlog({
        "incident_id": incident_id,
        "trusted_count": len(trusted_cmds),
        "untrusted_count": len(untrusted_cmds),
        "outputs_written": True,
    })

    print(f"[INFO] Phase-2 complete for {incident_id}\n", flush=True)

# --------------------------------------------------------------------
# Step 5: Kafka consumer entrypoint (auto Phase-2 trigger)
# --------------------------------------------------------------------

def consume_normalized_events():
    """
    Listen to Kafka topic 'incident.normalized' and trigger Phase-2 automatically.
    Runs continuously with periodic debug messages if no new events arrive.
    """
    topic = os.getenv("KAFKA_TOPIC_OUT", "incident.normalized")
    broker = os.getenv("KAFKA_BROKER", "localhost:9092")
    print(f"[INFO] Listening for normalized incidents on topic '{topic}' @ {broker}", flush=True)

    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[broker],
            auto_offset_reset="latest",
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            consumer_timeout_ms=5000,  # check more frequently
        )

        while True:
            found = False
            for msg in consumer:
                found = True
                payload = msg.value
                incident_id = payload.get("incident_id")
                if not incident_id:
                    print(f"[WARN] Invalid payload: {payload}", flush=True)
                    continue
                print(f"[INFO] Received normalized incident: {incident_id}", flush=True)
                run_phase2(incident_id)

            if not found:
                print("[DEBUG] No new normalized incidents; sleeping 10s...", flush=True)
                time.sleep(10)

    except Exception as exc:
        print(f"[ERROR] Kafka consumer loop error: {exc}\n{traceback.format_exc()}", flush=True)
        time.sleep(10)
    
# --------------------------------------------------------------------
# Step 6: CLI entrypoint & main
# --------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    # Mode 1: Direct CLI call → python phase2_interactive.py <incident_id>
    if len(sys.argv) == 2:
        incident_id = sys.argv[1]
        run_phase2(incident_id)
    else:
        # Mode 2: Kafka listener (auto Phase-2 trigger)
        consume_normalized_events()