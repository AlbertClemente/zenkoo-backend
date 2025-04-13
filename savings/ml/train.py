# Importamos pandas para manejar datos tabulares
import pandas as pd

# Importamos el vectorizador TF-IDF y el clasificador Naive Bayes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Creamos un pipeline de transformación + clasificación
from sklearn.pipeline import Pipeline

# Para guardar el modelo entrenado
import joblib

# Para obtener rutas relativas seguras
import os

def train_model():
    # Rutas
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Obtenemos la ruta de la carpeta actual (ml/)
    dataset_path = os.path.join(BASE_DIR, "dataset_kakeibo.csv")
    model_path = os.path.join(BASE_DIR, "model.pkl")

    # Leer el Dataset
    print("📥 Leyendo el dataset...")
    df = pd.read_csv(dataset_path)

    # Limpieza
    print("🧼 Limpiando datos...")
    df = df.dropna(subset=["type", "category"])
    df['type'] = df['type'].astype(str).str.strip()
    df['category'] = df['category'].astype(str).str.strip()
    df = df[df['type'] != ""]

    # Features y etiquetas
    # X = texto libre del gasto (ej: "Cena con amigos")
    # y = categoría asignada (ej: "Ocio y vicio")
    X = df['type']
    y = df['category']

    # Modelo
    print("⚙️ Entrenando el modelo...")
    # Creamos un pipeline que primero vectoriza el texto y luego entrena el clasificador
    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),      # Convierte el texto en vectores numéricos
        ('classifier', MultinomialNB())         # Clasifica usando Naive Bayes
    ])

    # Entrenamos el modelo con los datos del CSV para predecir la categoría a partir del tipo
    model.fit(X, y)

    # Guardar modelo
    print(f"💾 Guardando modelo en {model_path}...")
    joblib.dump(model, model_path) # Se guarda como archivo .pkl para usarlo en predict.py

    # Mensaje de confirmación
    print(f"✅ Modelo entrenado y guardado en {model_path}")

# Si ejecutamos el script directamente desde consola:
if __name__ == "__main__":
    train_model()