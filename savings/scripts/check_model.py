import os
import joblib


def check_model(model_path):
    # Verificar si el archivo .pkl existe
    if not os.path.exists(model_path):
        print(f"El archivo {model_path} no se encuentra.")
        return False

    try:
        # Intentamos cargar el modelo
        model = joblib.load(model_path)

        # Verificamos si el modelo tiene algún dato
        if model is None:
            print("El modelo está vacío.")
            return False

        # Aquí podemos agregar verificaciones adicionales dependiendo del modelo
        print("El modelo se cargó correctamente.")

        # Verificar si el modelo tiene el método 'predict'
        if hasattr(model, 'predict'):
            print("El modelo tiene un método 'predict', está listo para hacer predicciones.")
        else:
            print("El modelo no tiene el método 'predict'. Esto podría ser un problema.")

        # Inspeccionar los atributos del modelo
        print("\nAtributos del modelo:")
        print(dir(model))  # Imprime todos los atributos del modelo para inspección

        # Verificar si el modelo tiene un atributo como 'coef_' o 'intercept_', típicos en modelos lineales
        if hasattr(model, 'coef_'):
            print(f"Coeficientes del modelo: {model.coef_}")
        if hasattr(model, 'intercept_'):
            print(f"Intercepto del modelo: {model.intercept_}")

        # Comprobación del número de características (si se puede obtener)
        if hasattr(model, 'n_features_in_'):
            print(f"Número de características de entrada: {model.n_features_in_}")

        # Comprobar si el modelo tiene un atributo 'classes_' (común en clasificadores)
        if hasattr(model, 'classes_'):
            print(f"Clases del modelo: {model.classes_}")

        # Verificamos si el modelo tiene un atributo 'score' para evaluar la precisión
        if hasattr(model, 'score'):
            print("El modelo tiene un método 'score' para evaluación.")

        return True
    except Exception as e:
        print(f"Error al cargar el modelo: {str(e)}")
        return False


# Ruta donde está el archivo .pkl
model_path = './savings/static/ml/model.pkl'

# Test rápido

model = joblib.load(model_path)

# Test de predicción (suponiendo que 'text' es un dato que el modelo acepta)
text_to_predict = "Cena en restaurante"
prediction = model.predict([text_to_predict])

print(f"La predicción para '{text_to_predict}' es: {prediction[0]}")


# Llamar a la función para verificar el modelo
check_model(model_path)
