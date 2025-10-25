"""
Builds FAISS vector index (fields.vecdb) from canonical fields in synonyms.yaml.
Run once initially or weekly to refresh ontology embeddings.

Usage:
    python build_vecdb.py
"""

import os, yaml, faiss, numpy as np
from sentence_transformers import SentenceTransformer

# Paths from env or defaults
BASE_DIR = os.getenv("ONTOLOGY_DIR", "/app/shared/system/ontology")
SYN_PATH = os.path.join(BASE_DIR, "synonyms.yaml")
VEC_PATH = os.path.join(BASE_DIR, "fields.vecdb")
MODEL_NAME = os.getenv("ONTOLOGY_EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

print(f"[INFO] Building FAISS index from {SYN_PATH} using model {MODEL_NAME}")

with open(SYN_PATH, "r", encoding="utf-8") as fh:
    data = yaml.safe_load(fh) or {}

canon_fields = list(data.keys())
print(f"[INFO] Found {len(canon_fields)} canonical fields: {canon_fields}")

model = SentenceTransformer(MODEL_NAME)
embs = model.encode(canon_fields, normalize_embeddings=True)
embs = np.asarray(embs, dtype="float32")

index = faiss.IndexFlatIP(embs.shape[1])  # cosine similarity via dot product
index.add(embs)

faiss.write_index(index, VEC_PATH)
print(f"[OK] Saved FAISS index to {VEC_PATH}")
