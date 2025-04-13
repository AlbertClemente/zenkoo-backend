from savings.models import Expense
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIN_VALID_SAMPLES = 20  # Cambia este valor si quieres un umbral diferente

def retrain_model_from_db():
    print("📡 Consultando gastos con categoría...")

    all_expenses = Expense.objects.select_related('category').filter(category__isnull=False)

    print(f"🔎 Gastos encontrados: {len(all_expenses)}")

    valid_expenses = [
        expense for expense in all_expenses
        if expense.type and expense.type.strip() and expense.category and expense.category.name and expense.category.name.strip()
    ]

    print(f"✅ Gastos válidos para entrenamiento: {len(valid_expenses)}")

    if len(valid_expenses) < MIN_VALID_SAMPLES:
        print(f"⚠️ No hay suficientes datos para reentrenar. Se requieren al menos {MIN_VALID_SAMPLES}, hay {len(valid_expenses)}.")
        return

    # Creamos dataset
    data = pd.DataFrame([{
        'type': expense.type,
        'category': expense.category.name
    } for expense in valid_expenses])

    X = data['type']
    y = data['category']

    print("⚙️ Reentrenando modelo con datos reales...")

    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    model.fit(X, y)

    model_path = os.path.join(BASE_DIR, "model.pkl")

    print(f"💾 Guardando modelo en {model_path}...")
    joblib.dump(model, model_path)

    print(f"🎉 Modelo reentrenado con éxito usando {len(X)} registros.")

if __name__ == "__main__":
    retrain_model_from_db()