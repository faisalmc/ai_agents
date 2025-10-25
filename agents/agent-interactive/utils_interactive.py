"""
agents/interactive-agent/utils_interactive.py
--------------------
Utility functions used by the interactive-agent container across all phases.

Purpose:
- Provide helper routines for Phase 1–4 of interactive-agent.
- Handle common operations such as:
  * Directory creation for incidents
  * Loading YAML / JSON safely
  * Generating incident IDs
  * Writing and appending feedback logs
  * Publishing Kafka messages
  * Loading and using ontology vector index (FAISS / Chroma)
  * Device metadata lookup (vendor, platform, hostname)
  * Sending callbacks to the Orchestrator container

-----
“event received”, “normalized”, “IES written” logs == Implemented in consume_event, normalize_to_ies, and write_json
devices.yaml enrichment = Done via lookup_device_metadata() in utils.
issue_families.yaml keywords = Used to build few-shot LLM classification prompt.
ontology mapping with FAISS/Chroma = Called via ontology_map_fields() stub (FAISS integration later).
feedback JSONL append = For low confidence or errors (append_feedback).

"""

import os
import uuid
import json
import yaml
import datetime
import logging
import requests
from typing import Any, Dict, Tuple, Optional

# If FAISS or Chroma are not yet installed, later imports will be added here.
# For now we stub load_ontology_index() to avoid errors during early development.

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logger(name: str = "interactive_agent", level: str = "INFO") -> logging.Logger:
    """
    Create and return a logger with uniform formatting.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


logger = setup_logger()


# ---------------------------------------------------------------------------
# Directory and File Operations
# ---------------------------------------------------------------------------

def ensure_dirs(path: str) -> None:
    """
    Ensure that the directory path exists; create it if not.
    Auto-create directories.
    """
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as exc:
        logger.error(f"Failed to create directory {path}: {exc}")


def write_json(path: str, obj: Dict[str, Any]) -> None:
    """
    Write JSON data to a file with safe directory creation.
    Write structured JSON output.

    """
    try:
        ensure_dirs(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2)
        logger.info(f"JSON written: {path}")
    except Exception as exc:
        logger.error(f"Error writing JSON file {path}: {exc}")


def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    """
    Append one JSON record per line to a .jsonl feedback file.
    Append JSON lines to feedback.

    """
    try:
        ensure_dirs(os.path.dirname(path))
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception as exc:
        logger.error(f"Error appending to {path}: {exc}")


def load_yaml_safe(path: str) -> Dict[str, Any]:
    """
    Load YAML file safely; return empty dict on failure.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception as exc:
        logger.error(f"Failed to load YAML {path}: {exc}")
        return {}


# ---------------------------------------------------------------------------
# Incident and Feedback Helpers
# ---------------------------------------------------------------------------

def generate_incident_id() -> str:
    """
    Generate a unique incident ID.
    """
    return f"evt-{uuid.uuid4().hex[:8]}"


def append_feedback(event_type: str, payload: Dict[str, Any]) -> None:
    """
    Append feedback records (low-confidence, ontology alerts, etc.)
    into /shared/system/feedback/events-YYYYMMDD.jsonl
    """
    date_str = datetime.datetime.utcnow().strftime("%Y%m%d")
    feedback_root = os.getenv("FEEDBACK_PATH", "shared/system/feedback")
    path = os.path.join(feedback_root, f"events-{date_str}.jsonl")
    record = {"timestamp": datetime.datetime.utcnow().isoformat(), "type": event_type, **payload}
    append_jsonl(path, record)
    logger.info(f"Feedback appended: type={event_type} path={path}")


# ---------------------------------------------------------------------------
# Device Metadata Lookup
# ---------------------------------------------------------------------------

def lookup_device_metadata(device_name: str) -> Optional[Dict[str, str]]:
    """
    Enrich raw event with vendor/platform/hostname.

    Lookup vendor, platform, and hostname for a given device.

    This reads shared/system/reference/devices.yaml.
    Schema example:
      - name: A-RR-1
        hostname: 192.168.100.111
        username: cisco
        password: cisco
        device_type: cisco_ios
    """
    devices_file = os.getenv("DEVICES_YAML", "shared/system/reference/devices.yaml")
    data = load_yaml_safe(devices_file)
    devices = data if isinstance(data, list) else data.get("devices") or []

    for dev in devices:
        if str(dev.get("name", "")).strip() == device_name:
            vendor, platform = _map_device_type(dev.get("device_type"))
            return {
                "hostname": dev.get("hostname"),
                "vendor": vendor,
                "platform": platform,
            }
    return None


def _map_device_type(device_type: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert device_type to (vendor, platform).
    Mirrors orchestrator/slack_bot.py logic for consistency.
    basically consistent device type mapping logic.
    """
    dt = (device_type or "").strip().lower().replace("_", "-")
    if "iosxr" in dt:
        return "cisco", "iosxr"
    if "iosxe" in dt or dt in ("cisco-ios", "ios"):
        return "cisco", "iosxe"
    if "nxos" in dt:
        return "cisco", "nxos"
    if "juniper" in dt or "junos" in dt:
        return "juniper", "junos"
    if "arista" in dt or "eos" in dt:       # if dt in ("eos", "arista_eos", "arista-eos"):
        return "arista", "eos"
    return None, None


# ---------------------------------------------------------------------------
# Ontology Loader (FAISS / Chroma stub)
# ---------------------------------------------------------------------------

def ontology_map_fields(event_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
    """
    Map raw event keys to standardized field names using two methods:
      1) Exact keyword lookup from synonyms.yaml
      2) Semantic similarity lookup from fields.vecdb (FAISS)
    Returns a tuple: (mapped_fields, confidence_score)

    1- Reads synonyms.yaml and builds alias map --> {alias: canonical}
    2- Matches exact words (case-insensitive) --> fast and deterministic
    3- For unmatched keys, loads FAISS + SentenceTransformer --> semantic similarity
    4- If similarity ≥ threshold → maps; else logs alert --> creates one line per low-confidence field
    5- Confidence = total_matched / total_keys --> returned to caller
    """

    import yaml, faiss, numpy as np, json
    from sentence_transformers import SentenceTransformer
    from datetime import datetime

    # --- Load paths and settings from environment ---
    ontology_dir = os.getenv("ONTOLOGY_DIR", "/app/shared/system/ontology")
    synonyms_path = os.path.join(ontology_dir, "synonyms.yaml")
    vecdb_path = os.path.join(ontology_dir, "fields.vecdb")
    feedback_dir = os.getenv("FEEDBACK_PATH", "/app/shared/system/feedback")
    similarity_threshold = float(os.getenv("ONTOLOGY_FAISS_THRESHOLD", "0.8"))
    model_name = os.getenv("ONTOLOGY_EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # --- STEP 1: Load synonyms dictionary ---
    try:
        with open(synonyms_path, "r", encoding="utf-8") as fh:
            synonyms_data = yaml.safe_load(fh) or {}
    except Exception as exc:
        logger.warning(f"Could not load synonyms.yaml: {exc}")
        synonyms_data = {}

    # Build an alias → canonical dictionary for quick lookups
    alias_map = {}
    for canonical_field, aliases in synonyms_data.items():
        alias_map[canonical_field.lower()] = canonical_field
        for alias in (aliases or []):
            alias_map[alias.lower()] = canonical_field

    # --- STEP 2: First pass – exact synonym matches ---
    mapped_fields = {}
    unmatched_fields = []
    total_keys = 0
    matched_count = 0

    for raw_key, value in (event_dict or {}).items():
        total_keys += 1
        key_lower = str(raw_key).lower()
        canonical_field = alias_map.get(key_lower)
        if canonical_field:
            mapped_fields[canonical_field] = value
            matched_count += 1
        else:
            unmatched_fields.append((raw_key, value))

    # --- STEP 3: Second pass – semantic FAISS similarity for unmatched keys ---
    try:
        if unmatched_fields and os.path.exists(vecdb_path):
            # Load FAISS index and embedding model
            index = faiss.read_index(vecdb_path)
            model = SentenceTransformer(model_name)
            canonical_list = list(synonyms_data.keys())  # order matches embeddings in vecdb

            # Create embeddings for the unmatched field names
            unmatched_keys = [item[0] for item in unmatched_fields]
            query_vectors = model.encode(unmatched_keys, normalize_embeddings=True)
            query_vectors = np.asarray(query_vectors, dtype="float32")

            # Search for top-1 closest canonical field for each raw key
            similarities, indices = index.search(query_vectors, 1)

            for i, (raw_key, value) in enumerate(unmatched_fields):
                score = float(similarities[i][0])
                best_index = int(indices[i][0])
                best_field = canonical_list[best_index] if best_index < len(canonical_list) else None

                if best_field and score >= similarity_threshold:
                    mapped_fields[best_field] = value
                    matched_count += 1
                else:
                    mapped_fields[raw_key] = value
                    # Append a feedback entry for low-confidence match
                    os.makedirs(feedback_dir, exist_ok=True)
                    feedback_file = os.path.join(
                        feedback_dir, f"events-{datetime.now():%Y%m%d}.jsonl"
                    )
                    feedback_record = {
                        "type": "ontology_alert",
                        "key": raw_key,
                        "confidence": round(score, 3),
                    }
                    with open(feedback_file, "a", encoding="utf-8") as fb:
                        fb.write(json.dumps(feedback_record) + "\n")
        else:
            # If FAISS or model missing, keep unmatched keys unchanged
            for raw_key, value in unmatched_fields:
                mapped_fields[raw_key] = value

    except Exception as exc:
        logger.warning(f"Ontology FAISS similarity search failed: {exc}")
        # Fallback: keep original keys
        for raw_key, value in unmatched_fields:
            mapped_fields[raw_key] = value

    # --- STEP 4: Calculate overall mapping confidence ---
    confidence = matched_count / max(total_keys, 1)
    logger.info(f"Ontology mapping completed: confidence={confidence:.2f}")
    return mapped_fields, confidence


# ---------------------------------------------------------------------------
# Kafka and Orchestrator Communications
# ---------------------------------------------------------------------------

def publish_kafka(topic: str, payload: Dict[str, Any]) -> None:
    """
    Publish payload to Kafka topic (e.g., incident.normalized).
    Placeholder implementation until integrated with kafka-python.
    """
    logger.info(f"[Kafka Publish] topic={topic} payload_keys={list(payload.keys())}")


def notify_orchestrator(event_type: str, payload: Dict[str, Any]) -> None:
    """
    Send callback event to Orchestrator container, which will then
    format and post messages to Slack.

    The URL is read from ORCH_CALLBACK_URL in .env.
    """
    orch_url = os.getenv("ORCH_CALLBACK_URL")
    if not orch_url:
        logger.warning("ORCH_CALLBACK_URL not set; skipping orchestrator callback.")
        return
    try:
        requests.post(f"{orch_url}/events/update", json={"type": event_type, "data": payload}, timeout=3)
        logger.info(f"Orchestrator notified: {event_type}")
    except Exception as exc:
        logger.warning(f"Failed to notify orchestrator: {exc}")