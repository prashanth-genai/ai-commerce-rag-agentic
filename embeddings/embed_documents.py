from sentence_transformers import SentenceTransformer
import faiss
import json
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = []
sources = ["data/products.json", "data/pricing_rules.json", "data/return_policy.txt"]

for file in sources:
    with open(file) as f:
        if file.endswith(".json"):
            docs.extend(json.load(f))
        else:
            docs.append({"content": f.read()})

texts = [str(doc) for doc in docs]
embeddings = model.encode(texts)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

faiss.write_index(index, "vector_store/faiss_index/index.bin")
print("Embeddings created successfully")

