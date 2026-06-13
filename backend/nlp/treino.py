import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from dataset_generator import gerar_dataset

TEXTO_PATH = "dataset_textos.pkl"
LABEL_PATH = "dataset_labels.pkl"
VECTORIZER_PATH = "vectorizer.pkl"
MODEL_PATH = "modelo.pkl"

def treinar():
    print("Gerando dataset...")
    textos, labels = gerar_dataset()
    with open(TEXTO_PATH, "wb") as f:
        pickle.dump(textos, f)
    with open(LABEL_PATH, "wb") as f:
        pickle.dump(labels, f)

    print("Vectorizando textos...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(textos)

    print("Treinando modelo...")
    model = LogisticRegression(max_iter=1000)
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    acuracia = model.score(X_test, y_test)
    print(f"Acurácia: {acuracia:.4f}")

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Modelo treinado e salvo com sucesso!")

if __name__ == "__main__":
    treinar()
