from savings.models import Expense
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def retrain_model_from_db():
    # Traemos solo gastos con categoría definida
    all_expenses = Expense.objects.select_related('category').filter(category__isnull=False)

    # Filtramos: que tengan type válido y category.name válido
    valid_expenses = [
        expense for expense in all_expenses
        if expense.type and expense.type.strip() and expense.category and expense.category.name and expense.category.name.strip()
    ]

    if not valid_expenses:
        print("No hay gastos válidos para entrenar.")
        return

    # Creamos dataset con el nombre de la categoría
    data = pd.DataFrame([{
        'type': expense.type,
        'category': expense.category.name
    } for expense in valid_expenses])

    X = data['type']
    y = data['category']

    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    model.fit(X, y)

    model_path = os.path.join(BASE_DIR, "model.pkl")
    joblib.dump(model, model_path)

    print(f"Modelo reentrenado con {len(X)} registros y guardado en {model_path}")