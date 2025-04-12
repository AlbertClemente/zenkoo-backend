import os
import joblib

# Obtenemos la ruta de la carpeta actual (ml/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta al archivo del modelo entrenado
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Cargamos el modelo al iniciar el módulo (para no cargarlo cada vez)
model = None

def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("El archivo del modelo no existe. Entrena el modelo primero.")
        model = joblib.load(MODEL_PATH)

# Función para predecir la categoría según el tipo
def predict_category(type_text: str) -> str:
    load_model()  # Cargamos el modelo si aún no está cargado
    prediction = model.predict([type_text])  # Predecimos con un array
    return prediction[0]  # Devolvemos la categoría predicha (string)