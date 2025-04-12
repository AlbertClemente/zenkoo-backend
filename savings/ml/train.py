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

# Obtenemos la ruta de la carpeta actual (ml/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def train_model():
    # Cargamos el dataset CSV desde la ruta relativa
    dataset_path = os.path.join(BASE_DIR, "dataset_kakeibo.csv")
    df = pd.read_csv(dataset_path)

    # X = texto libre del gasto (ej: "Cena con amigos")
    # y = categoría asignada (ej: "Ocio y vicio")
    X = df['type']
    y = df['category']

    # Creamos un pipeline que primero vectoriza el texto y luego entrena el clasificador
    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),      # Convierte el texto en vectores numéricos
        ('classifier', MultinomialNB())         # Clasifica usando Naive Bayes
    ])

    # Entrenamos el modelo con los datos del CSV para predecir la categoría a partir del tipo
    model.fit(X, y)

    # Guardamos el modelo entrenado como archivo .pkl para usarlo en predict.py
    model_path = os.path.join(BASE_DIR, "model.pkl")
    joblib.dump(model, model_path)

    # Mensaje de confirmación
    print(f"Modelo entrenado y guardado en {model_path}")

# Si ejecutamos el script directamente desde consola:
if __name__ == "__main__":
    train_model()