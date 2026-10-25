from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class ReviewSentimentService:
    def __init__(self):
        texts = [
            "excellent product fast delivery very happy",
            "great quality works perfectly love it",
            "comfortable and reliable would buy again",
            "terrible quality stopped working",
            "bad battery and very disappointing",
            "late delivery damaged product poor experience",
            "good screen but battery is weak",
            "average product nothing special",
        ]
        labels = [1, 1, 1, 0, 0, 0, 0, 1]
        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=500)),
        ]).fit(texts, labels)

    def analyze(self, text: str):
        positive = float(self.model.predict_proba([text])[0, 1])
        return {
            "sentiment": "POSITIVE" if positive >= 0.5 else "NEGATIVE",
            "positive_probability": round(positive, 4),
            "note": "Educational small-data NLP baseline; production review intelligence needs larger labeled data and aspect extraction.",
        }
