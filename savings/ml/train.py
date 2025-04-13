# Importamos pandas para manejar datos tabulares
import pandas as pd

# Importamos el vectorizador TF-IDF y el clasificador Naive Bayes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Pipeline de transformación + clasificación
from sklearn.pipeline import Pipeline

# Para guardar el modelo entrenado
import joblib

# Para trabajar con rutas, JSON y fechas
import os
import json
from datetime import datetime

# Para evaluar el modelo
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta /ml/
STATIC_ML_DIR = os.path.join(BASE_DIR, '..', 'static', 'ml')
os.makedirs(STATIC_ML_DIR, exist_ok=True)

def save_model_info(categories, accuracy, sample_count):
    info = {
        "lastTrainedAt": datetime.now().isoformat(),
        "sampleCount": sample_count,
        "categories": categories,
        "accuracy": accuracy,
        "modelVersion": str(datetime.now().timestamp())
    }

    with open(os.path.join(STATIC_ML_DIR, "model_info.json"), "w") as f:
        json.dump(info, f)


def train_model():
    dataset_path = os.path.join(BASE_DIR, "dataset_kakeibo.csv")
    model_path = os.path.join(STATIC_ML_DIR, "model.pkl")

    print("📥 Leyendo el dataset...")
    df = pd.read_csv(dataset_path)

    print("🧼 Limpiando datos...")
    df = df.dropna(subset=["type", "category"])
    df['type'] = df['type'].astype(str).str.strip()
    df['category'] = df['category'].astype(str).str.strip()
    df = df[df['type'] != ""]

    X = df['type']
    y = df['category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("⚙️ Entrenando el modelo...")
    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"📈 Accuracy: {accuracy:.4f}")

    print(f"💾 Guardando modelo en {model_path}...")
    joblib.dump(model, model_path)

    save_model_info(
        categories=sorted(list(set(y))),
        accuracy=round(accuracy, 4),
        sample_count=len(y)
    )

    print("✅ Entrenamiento completo.")


if __name__ == "__main__":
    train_model()
