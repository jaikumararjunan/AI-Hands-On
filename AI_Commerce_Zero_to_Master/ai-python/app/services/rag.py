from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RagService:
    def __init__(self):
        knowledge_dir = Path(__file__).resolve().parent.parent / "knowledge"
        self.docs = []
        for path in sorted(knowledge_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for i, chunk in enumerate(self._chunk(text)):
                self.docs.append({"source": path.name, "chunk": i, "text": chunk})
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in self.docs])

    @staticmethod
    def _chunk(text: str, words_per_chunk: int = 120):
        words = text.split()
        return [" ".join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]

    def retrieve(self, query: str, limit: int = 3):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:limit]
        return [dict(self.docs[i], score=round(float(score), 4)) for i, score in ranked]
