from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.catalog import PRODUCTS

class SemanticSearchService:
    """Educational baseline: TF-IDF semantic-ish search. Replace with embeddings + vector DB in production."""
    def __init__(self):
        self.docs = [f"{p['name']} {p['category']} {p['brand']} {p['description']}" for p in PRODUCTS]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.docs)

    def search(self, query: str, limit: int = 5):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:limit]
        return [
            {"product_id": PRODUCTS[i]["id"], "name": PRODUCTS[i]["name"], "score": round(float(score), 4)}
            for i, score in ranked
        ]
