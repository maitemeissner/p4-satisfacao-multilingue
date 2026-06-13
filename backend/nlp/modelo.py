from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
import joblib
import os
import numpy as np

MODEL_PATH = "backend/nlp/modelo.pkl"
VECTORIZER_PATH = "backend/nlp/vectorizer.pkl"

POSITIVOS_PT = ["ótimo", "excelente", "maravilhoso", "bom", "recomendo", "gostei", "perfeito", "amo", "adoro", "top"]
NEGATIVOS_PT = ["péssimo", "horrível", "ruim", "não gostei", "decepcionante", "terrível", "frustrante", "lento", "cara"]
POSITIVOS_EN = ["great", "excellent", "wonderful", "good", "recommend", "loved", "perfect", "amazing", "fantastic"]
NEGATIVOS_EN = ["terrible", "horrible", "bad", "awful", "disappointing", "poor", "worst", "hate", "slow"]
POSITIVOS_ES = ["excelente", "maravilloso", "bueno", "recomiendo", "encantó", "perfecto", "increíble", "genial"]
NEGATIVOS_ES = ["pésimo", "horrible", "malo", "decepcionante", "terrible", "frustrante", "lento", "caro"]

def gerar_dados_treino():
    textos, scores = [], []
    for p in POSITIVOS_PT + POSITIVOS_EN + POSITIVOS_ES:
        textos.append(p); scores.append(5.0)
    for n in NEGATIVOS_PT + NEGATIVOS_EN + NEGATIVOS_ES:
        textos.append(n); scores.append(1.0)
    return textos, scores

def treinar():
    textos, scores = gerar_dados_treino()
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(textos)
    model = Ridge(alpha=1.0)
    model.fit(X, scores)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    return model, vectorizer

def predict_score(texto: str, idioma: str = "pt-BR") -> float:
    if not os.path.exists(MODEL_PATH):
        model, vectorizer = treinar()
    else:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)

    X = vectorizer.transform([texto])
    score = model.predict(X)[0]
    return round(max(1.0, min(5.0, score)), 2)

if __name__ == "__main__":
    treinar()
    print("Modelo treinado com sucesso!")