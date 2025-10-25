"""
build_vecdb.py
--------------
Builds FAISS vector index (fields.vecdb) from canonical fields in synonyms.yaml.
Run once initially or weekly to refresh ontology embeddings.
Author: Faisal Chaudhry

Usage:
  python build_vecdb.py
"""

import os, yaml, json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime

ONTOLOGY_DIR = "/app/shared/system/ontology"
SYNONYMS_YAML = os.path.join(ONTOLOGY_DIR, "synonyms.yaml")
VECDB_PATH = os.path.join(ONTOLOGY_DIR, "fields.vecdb")
META_PATH = os.path.join(ONTOLOGY_DIR, "fields.meta.json")

model = SentenceTransformer("all-MiniLM-L6-v2")

def log(msg): print(f"[build_vecdb] {msg}")

def build_index():
    if not os.path.exists(SYNONYMS_YAML):
        log(f"ERROR: File not found → {SYNONYMS_YAML}")
        return

    with open(SYNONYMS_YAML, "r", encoding="utf-8") as fh:
        synonyms = yaml.safe_load(fh) or {}

    if not synonyms:
        log("ERROR: No entries in synonyms.yaml")
        return

    canonical, phrases = [], []
    for canon, alias_list in synonyms.items():
        canonical.append(canon)
        all_terms = [canon] + list(alias_list or [])
        phrases.extend(all_terms)

    log(f"Loaded {len(canonical)} canonical fields, {len(phrases)} total phrases")

    # Create embeddings
    try:
        emb = model.encode(phrases, normalize_embeddings=True)
    except Exception as e:
        log(f"Embedding failed: {e}")
        return

    d = emb.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(np.array(emb).astype("float32"))

    faiss.write_index(index, VECDB_PATH)
    meta = {"fields": canonical, "phrases": phrases, "built_at": f"{datetime.utcnow():%Y-%m-%dT%H:%M:%SZ}"}
    with open(META_PATH, "w", encoding="utf-8") as m:
        json.dump(meta, m, indent=2)

    log(f"✅ FAISS index written to {VECDB_PATH}")
    log(f"✅ Metadata written to {META_PATH}")

if __name__ == "__main__":
    try:
        build_index()
    except Exception as e:
        log(f"Unhandled error: {e}")