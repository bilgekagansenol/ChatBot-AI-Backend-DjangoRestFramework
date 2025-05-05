import pickle
from loader import load_people_data

from sentence_transformers import SentenceTransformer


# 1. Embedder modeli indir
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Veriyi JSON'dan çek
people = load_people_data("rag_data/people_data.json")

print("Yüklenen people verisi:")
print(people)

# 3. Embedlenecek metinleri oluştur
corpus = [p["content"] for p in people]
metadata = [{"id": p["id"]} for p in people]

# 4. Vektörleri oluştur
embeddings = model.encode(corpus, convert_to_tensor=True)

# 5. Kaydet
with open("rag_data/embeddings.pkl", "wb") as f:
    pickle.dump({
        "embeddings": embeddings,
        "corpus": corpus,
        "metadata": metadata
    }, f)

print("Embedding işlemi başarıyla tamamlandı.")
