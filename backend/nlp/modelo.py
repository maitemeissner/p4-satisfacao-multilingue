import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

CLASSES = ["Muito Ruim", "Ruim", "Regular", "Bom", "Excelente"]

class ModeloPreditor:
    def __init__(self):
        self.vectorizer: TfidfVectorizer | None = None
        self.model: LogisticRegression | None = None
        self._carregar_ou_criar()

    def _carregar_ou_criar(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            with open(VECTORIZER_PATH, "rb") as f:
                self.vectorizer = pickle.load(f)
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
        else:
            self._criar_mock()

    def _criar_mock(self):
        textos = [
            "Ótimo produto, adorei",
            "Muito bom, recomendo",
            "Bom, atendeu minhas expectativas",
            "Mais ou menos, poderia ser melhor",
            "Ruim, não gostei",
            "Péssimo, horrível",
            "Great product, I love it",
            "Very good, recommended",
            "Excellent service",
            "Not bad, could be better",
            "Terrible experience",
            "Excelente producto, me encanta",
            "Buen servicio, lo recomiendo",
            "Malo, no me gustó",
            "Regular, esperaba más",
            "Amazing quality, will buy again",
            "Horrible, waste of money",
            "Fantástico, superou expectativas",
            "Decepcionante, não vale a pena",
            "Muy malo, pésimo",
        ]
        scores = [5, 5, 4, 3, 2, 1, 5, 4, 5, 3, 1, 5, 4, 2, 3, 5, 1, 5, 2, 1]
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(textos)
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, scores)
        with open(VECTORIZER_PATH, "wb") as f:
            pickle.dump(self.vectorizer, f)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)

    def prever(self, texto: str) -> tuple[float, str, float]:
        if not self.vectorizer or not self.model:
            return (3.0, "Regular", 0.5)
        X = self.vectorizer.transform([texto])
        score = int(self.model.predict(X)[0])
        probas = self.model.predict_proba(X)[0]
        confianca = float(np.max(probas))
        if score < 1:
            score = 1
        elif score > 5:
            score = 5
        classe = CLASSES[score - 1]
        return (float(score), classe, confianca)
