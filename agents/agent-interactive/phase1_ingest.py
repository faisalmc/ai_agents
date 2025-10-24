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
    Enrich event with vendor/platform/hostname information
    from shared/system/reference/devices.yaml.
    """
    ip = str(event.get("ip") or event.get("source_ip") or "")
    name = event.get("device_name") or event.get("hostname") or ""
    device_info = lookup_device_metadata(name)
    if device_info:
        event["source"] = {
            "hostname": device_info.get("hostname"),
            "vendor": device_info.get("vendor"),
            "platform": device_info.get("platform"),
        }
        logger.info(f"Device enriched: {name} → {device_info}")
    else:
        logger.warning(f"No device match found for {name or ip}")
    return event


# ---------------------------------------------------------------------------
# Step 3 – Family Classification
# ---------------------------------------------------------------------------

def classify_family(symptom_text: str) -> str:
    """
    Use LLM to classify the issue family (interface, routing, cpu, config, etc.)
    using keywords from issue_families.yaml.
    """
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

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages=messages, temperature=0)  # NOTE: messages=..., not prompt=
        family = (response or "").strip().split()[0].lower()

        # Keep result constrained to known families
        if family not in issue_families.keys():
            logger.warning(f"Unrecognized family from LLM: {family}")
            family = "unknown"
        return family
    except Exception as exc:
        logger.error(f"Family classification failed: {exc}")
        return "unknown"

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
            "Given the raw event JSON and mapped field names, "
            "produce a normalized Incident Event Schema JSON object. "
            "Use required and optional fields from the family specification.\n\n"
            f"Family spec: {json.dumps(family_spec)}\n\n"
            f"Raw event: {json.dumps(event)}"
        )

        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages=messages, temperature=0)  # NOTE: messages=..., not prompt=
        ies_json = json.loads(response)
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
            notify_orchestrator("incident_normalized", {"incident_id": incident_id, "family": family, "confidence": confidence})
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
            logger.error("No event loaded; exiting.")
            return

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

        # LLM normalization
        ies_json = normalize_to_ies(event, family)
        if not ies_json:
            logger.error("Normalization failed; aborting.")
            return

        norm_path = os.path.join(ingest_dir, "1.2-normalized.json")
        write_json(norm_path, ies_json)
        logger.info(f"IES written: path={norm_path}")

        # Validation & publish
        validate_and_publish(incident_id, ies_json, family)

    except Exception as exc:
        logger.error(f"Unhandled exception in Phase-1: {exc}\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()