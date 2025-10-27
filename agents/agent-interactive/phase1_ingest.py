"""
agents/interactive-agent/phase1_ingest.py
----------------
Implements Phase-1 of interactive-agent:
Convert raw network events (Kafka or simulated JSON) into a normalized
Incident Event Schema (IES) record ready for validation in Phase-2.

Workflow Steps:
1. Event intake (Kafka or mock file)
2. Device enrichment using devices.yaml
3. Family classification (LLM)
4. Ontology field mapping (FAISS/Chroma)
5. LLM normalization → structured IES JSON
6. Validation and feedback
7. Publish to Kafka (incident.normalized) and notify orchestrator
"""

import os
import json
import datetime
import time
import traceback
from typing import Dict, Any, Optional
from utils_interactive import (
    setup_logger,
    ensure_dirs,
    write_json,
    load_yaml_safe,
    generate_incident_id,
    append_feedback,
    lookup_device_metadata,
    ontology_map_fields,
    publish_kafka,
    notify_orchestrator,
)
from shared.llm_api import call_llm
from kafka import KafkaConsumer # for kafka consumer message

logger = setup_logger("phase1_ingest", os.getenv("LOG_LEVEL", "INFO"))

# ---------------------------------------------------------------------------
# Load reference catalogs once at startup
# ---------------------------------------------------------------------------

ISSUE_FAMILIES_PATH = os.getenv("ISSUE_FAMILIES", "shared/system/reference/issue_families.yaml")
DEVICES_YAML_PATH = os.getenv("DEVICES_YAML", "shared/system/reference/devices.yaml")
INCIDENT_ROOT = os.getenv("INCIDENT_ROOT", "agents/interactive-agent/incidents")
KAFKA_TOPIC_OUT = os.getenv("KAFKA_TOPIC_OUT", "incident.normalized")

issue_families = load_yaml_safe(ISSUE_FAMILIES_PATH)


# ---------------------------------------------------------------------------
# Step 1 – Event Intake
# ---------------------------------------------------------------------------

def consume_event() -> Dict[str, Any]:
    """
    Read a raw event either from Kafka or mock JSON file.

    MODE=mock  → loads /input/events-simulated/sample.json
    MODE=kafka → reads one JSON message from the Kafka topic defined in .env

    Returns:
        dict: Parsed event payload.
    """
    mode = os.getenv("MODE", "mock").lower()
    event: Dict[str, Any] = {}

    try:
        if mode == "mock":
            mock_path = os.getenv("MOCK_EVENT_PATH", "input/events-simulated/sample.json")
            with open(mock_path, "r", encoding="utf-8") as fh:
                event = json.load(fh)
            logger.info(f"event received: mode=mock source={mock_path}")

        elif mode == "kafka":
            topic = os.getenv("KAFKA_TOPIC_IN", "network.events.raw")
            broker = os.getenv("KAFKA_BROKER", "localhost:9092")
            #  KAFKA_TOPIC_IN = name of the Kafka topic that Phase-1 subscribes to — the “mailbox” where upstream systems drop raw network events.

            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[broker],
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                consumer_timeout_ms=10000,   # stop if nothing received
            )

            logger.info(f"Listening to Kafka topic '{topic}' on broker '{broker}'...")
            for msg in consumer:
                event = msg.value
                logger.info(
                    f"event received: mode=kafka topic={topic} "
                    f"partition={msg.partition} offset={msg.offset}"
                )
                break  # read only one message for now
            consumer.close()

        else:
            logger.warning(f"Unknown MODE '{mode}'; no event consumed.")

    except Exception as exc:
        logger.error(f"Failed to read input event: {exc}")

    return event

# ---------------------------------------------------------------------------
# Step 2 – Device Enrichment
# ---------------------------------------------------------------------------

def enrich_device(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich event with hostname (friendly name), IP, vendor, and platform
    from shared/system/reference/devices.yaml.

    - devices.yaml 'name'  → friendly hostname (A-PE-1)
    - devices.yaml 'hostname' → management IP (192.168.100.101)
    """
    ip = str(event.get("ip") or event.get("source_ip") or "").strip()
    name = str(event.get("device_name") or event.get("hostname") or "").strip()

    # Try lookup by name, then IP
    device_info = lookup_device_metadata(name) or (lookup_device_metadata(ip) if ip else None)

    if device_info:
        event["source"] = {
            "hostname": device_info.get("hostname") or name or ip,  # friendly name
            "ip": device_info.get("ip") or ip,
            "vendor": device_info.get("vendor"),
            "platform": device_info.get("platform"),
        }
        logger.info(
            f"Device enriched: name={name or ip}, "
            f"hostname={event['source']['hostname']}, "
            f"ip={event['source']['ip']}, "
            f"vendor={event['source']['vendor']}, "
            f"platform={event['source']['platform']}"
        )
    else:
        # Fallback to avoid empty source block
        event["source"] = {
            "hostname": name or ip,
            "ip": ip,
            "vendor": "unknown",
            "platform": "unknown",
        }
        logger.warning(f"No device match found for {name or ip}; applied fallback: {event['source']}")

    # --- Optional enrichment summary log for visibility ---
    src = event.get("source", {})
    logger.info(
        f"[Enrichment Summary] Hostname={src.get('hostname')}, "
        f"IP={src.get('ip')}, Vendor={src.get('vendor')}, Platform={src.get('platform')}"
    )

    return event

# ---------------------------------------------------------------------------
# Step 3 – Family Classification
# ---------------------------------------------------------------------------

def classify_family(symptom_text: str) -> str:
    """
    Use LLM to classify the issue family (interface, routing, cpu, config, etc.)
    using keywords from issue_families.yaml.
    """

    family = "unknown"   # <-- define default early

    try:
        examples = []
        for fam, spec in issue_families.items():
            kws = ", ".join(spec.get("keywords", []))
            examples.append(f"{fam}: {kws}")
        prompt = (
            "Classify the issue family for the following symptom text.\n"
            "Families and sample keywords:\n" + "\n".join(examples) +
            f"\n\nSymptom: {symptom_text}\n"
            "Respond with only one family name from the list above."
        )

        # --- DEBUG LOGGING ---
        logger.debug(f"[LLM FAMILY PROMPT] ===\n{prompt}\n=== END PROMPT ===")

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages=messages, temperature=0)  # NOTE: messages=..., not prompt=

        # --- DEBUG LOGGING OF RESPONSE ---
        logger.debug(f"[LLM FAMILY RESPONSE] {response[:200]}")

        # Extract first word of response as the family label
        if response:
            family = (response or "").strip().split()[0].lower()

        if family not in issue_families.keys():
            logger.warning(f"[FamilyClassifier] Unrecognized family from LLM: {family}")
            family = "unknown"

        logger.info(f"[FamilyClassifier] LLM selected family='{family}' for symptom='{symptom_text[:80]}'")

    except Exception as exc:
        logger.error(f"[FamilyClassifier] Failed: {exc}")
        family = "unknown"
    
    return family

# ---------------------------------------------------------------------------
# Step 4 – Ontology Field Mapping
# ---------------------------------------------------------------------------

def map_event_fields(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map raw keys to canonical schema fields using ontology (FAISS/Chroma).
    """
    try:
        mapped, conf = ontology_map_fields(event)
        event["mapped_fields"] = mapped
        if conf < 0.8:
            append_feedback("ontology_alert", {"confidence": conf, "fields": list(mapped.keys())})
            logger.warning(f"Ontology mapping confidence low ({conf})")
        else:
            logger.info(f"Ontology mapping complete (conf={conf})")
    except Exception as exc:
        logger.error(f"Ontology mapping error: {exc}")
    return event


# ---------------------------------------------------------------------------
# Step 5 – LLM Normalization
# ---------------------------------------------------------------------------

def normalize_to_ies(event: Dict[str, Any], family: str) -> Optional[Dict[str, Any]]:
    """
    Build prompt for LLM normalization according to family_spec.
    Output must follow agreed Incident Event Schema.
    """
    try:
        family_spec = issue_families.get(family, {})
        prompt = (
            "You are a system that converts raw network events into a normalized Incident Event Schema (IES). "
            "Respond ONLY with a valid JSON object — do not include explanations, text, or markdown. "
            "The JSON must include a 'family' object with the following structure:\n"
            "{\n"
            "  'family': {\n"
            "     'type': '<family_name>',\n"
            "     <required and optional fields from the spec>\n"
            "  },\n"
            "  'confidence': <0.0-1.0>\n"
            "}\n\n"
            f"Family spec: {json.dumps(family_spec)}\n\n"
            f"Raw event: {json.dumps(event)}"
        )

        # Log what the LLM is being asked
        logger.debug(f"[LLM PROMPT] ===\n{prompt}\n=== END PROMPT ===")

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages=messages, temperature=0)  # NOTE: messages=..., not prompt=

        # logging to check LLM response in JSON format or not
        logger.debug(f"LLM raw response: {response[:500]}")

        ies_json = json.loads(response)
        logger.info(f"LLM normalization successful for family={family}")
        return ies_json

    except Exception as exc:
        logger.error(f"LLM normalization failed: {exc}")
        append_feedback("llm_normalization_error", {"error": str(exc)})
        return None


# ---------------------------------------------------------------------------
# Step 6 – Validation & Feedback
# ---------------------------------------------------------------------------

def validate_and_publish(incident_id: str, ies: Dict[str, Any], family: str) -> None:
    """
    Validate IES fields based on issue_families.yaml.
    Append feedback if required fields missing or confidence low.
    Publish event ID to Kafka for next phase and notify orchestrator.
    """
    try:
        spec = issue_families.get(family, {})
        required = set(spec.get("required", []))
        present = set(ies.get("family", {}).keys())
        missing = list(required - present)
        confidence = float(ies.get("confidence", 1.0))

        if missing or confidence < 0.6:
            append_feedback("parser_alert", {"incident_id": incident_id, "missing": missing, "confidence": confidence})
            logger.warning(f"Validation failed: missing={missing} conf={confidence}")
        else:
            publish_kafka(KAFKA_TOPIC_OUT, {"incident_id": incident_id})
            # debugging -- before calling notify_orchestrator #
            logger.debug(f"[PublishToOrch] IES Source: {json.dumps(ies.get('source', {}), indent=2)}")
            notify_orchestrator(
                "incident_normalized",
                {
                    "incident_id": incident_id,
                    "family": family,
                    "confidence": confidence,
                    "severity": ies.get("context", {}).get("severity"),
                    "hostname": ies.get("source", {}).get("hostname"),
                    "ip": ies.get("source", {}).get("ip"),
                    "symptom": ies.get("symptom_text"),
                    "timestamp": ies.get("context", {}).get("timestamp")
                }
            )
            logger.info(f"Validation passed and event published: id={incident_id}")
    except Exception as exc:
        logger.error(f"Validation error: {exc}")


# ---------------------------------------------------------------------------
# Main Execution Flow
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Orchestrate the full Phase-1 ingestion and normalization flow.
    """
    try:
        event = consume_event()
        if not event:
            # logger.error("No event loaded; exiting.")
            # return
            logger.debug("No new events from Kafka; sleeping 10s...")
            time.sleep(10)
            continue

        incident_id = generate_incident_id()
        ingest_dir = os.path.join(INCIDENT_ROOT, incident_id, "1-ingest")
        ensure_dirs(ingest_dir)

        raw_path = os.path.join(ingest_dir, "1.1-raw.json")
        write_json(raw_path, event)

        # Device enrichment
        event = enrich_device(event)

        # Extract symptom text
        symptom_text = event.get("symptom") or event.get("message") or json.dumps(event)
        family = classify_family(symptom_text)
        event["family_type"] = family

        # Ontology mapping
        event = map_event_fields(event)

        # LLM normalization (returns {'family': {...}, 'confidence': ...})
        ies_partial = normalize_to_ies(event, family)
        if not ies_partial:
            logger.error("Normalization failed; aborting.")
            return

        # Compose the full IES so we never drop critical context
        ies_full = compose_final_ies(
            incident_id=incident_id,
            raw_event=event,      # already enriched in Step-2
            family_type=family,
            llm_out=ies_partial
        )

        norm_path = os.path.join(ingest_dir, "1.2-normalized.json")
        write_json(norm_path, ies_full)
        logger.info(f"IES written: path={norm_path}")

        # Validation & publish use the full IES (validator already reads ies['family'])
        validate_and_publish(incident_id, ies_full, family)

    except Exception as exc:
        logger.error(f"Unhandled exception in Phase-1: {exc}\n{traceback.format_exc()}")
        time.sleep(5)

# ------------------------------------------ #
# --- Final IES = Merging enrichment (Device/platform) + Raw_context + LLM_family_block --- #
def compose_final_ies(
    incident_id: str,
    raw_event: Dict[str, Any],
    family_type: str,
    llm_out: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build the final IES by combining:
      - enrichment from raw_event['source'] (hostname/vendor/platform)
      - raw context (ip, severity, timestamp, symptom/message)
      - LLM output for the 'family' block + confidence
    """
    # Pull enrichment (added earlier in Step-2)
    source = raw_event.get("source") or {}
    hostname = source.get("hostname") or raw_event.get("device_name") or ""
    vendor   = source.get("vendor") or ""
    platform = source.get("platform") or ""
    ip       = source.get("ip") or raw_event.get("ip") or ""

    # Context from raw event
    severity  = raw_event.get("severity") or ""
    timestamp = raw_event.get("timestamp") or ""
    symptom   = raw_event.get("symptom") or raw_event.get("message") or ""

    # LLM output (already contains 'family' and optionally 'confidence')
    family_block = (llm_out or {}).get("family") or {}
    family_block["type"] = family_type  # enforce the classified family

    # Confidence from LLM (fallback to 1.0)
    try:
        confidence = float((llm_out or {}).get("confidence", 1.0))
    except Exception:
        confidence = 1.0

    ies = {
        "incident_id": incident_id,
        "source": {
            "hostname": hostname,
            "ip": ip,
            "vendor": vendor,
            "platform": platform,
        },
        "context": {
            "severity": severity,
            "timestamp": timestamp,
            "event_class": family_type,
        },
        "symptom_text": symptom,
        "family": family_block,
        "confidence": confidence,
    }
    return ies

if __name__ == "__main__":
    main()