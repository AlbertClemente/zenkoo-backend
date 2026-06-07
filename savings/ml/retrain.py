import logging

from savings.models import Expense
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import json
from datetime import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIN_VALID_SAMPLES = 20  # Umbral mínimo para reentrenar
STATIC_ML_DIR = os.path.join(BASE_DIR, '..', 'static', 'ml')

# Nos aseguramos que que la carpeta ml/ existe antes de guardar:
os.makedirs(STATIC_ML_DIR, exist_ok=True)

logger = logging.getLogger(__name__)


class NotEnoughDataError(Exception):
    def __init__(self, detail):
        self.code = "NOT_ENOUGH_DATA"
        self.detail = detail


def save_model_info(categories, accuracy, sample_count, category_distribution=None):
    if category_distribution is None:
        category_distribution = {}

    info = {
        "lastTrainedAt": datetime.now().isoformat(),
        "sampleCount": sample_count,
        "categories": categories or [],
        "accuracy": accuracy,
        "modelVersion": str(datetime.now().timestamp()),
        "categoryDistribution": category_distribution
    }

    with open(os.path.join(STATIC_ML_DIR, 'model_info.json'), "w") as f:
        json.dump(info, f)


def retrain_model_from_db():
    logger.info("Consultando gastos con categoría...")

    all_expenses = Expense.objects.select_related('category').filter(category__isnull=False)

    logger.info("Gastos encontrados: %d", len(all_expenses))

    valid_expenses = [
        expense for expense in all_expenses
        if expense.type and expense.type.strip() and expense.category and expense.category.name and expense.category.name.strip()
    ]

    logger.info("Gastos válidos para entrenamiento: %d", len(valid_expenses))

    if len(valid_expenses) < MIN_VALID_SAMPLES:
        raise NotEnoughDataError(
            f"No hay suficientes datos para reentrenar. Se requieren al menos {MIN_VALID_SAMPLES}, hay {len(valid_expenses)}."
        )

    # Dataset
    data = pd.DataFrame([{
        'type': expense.type,
        'category': expense.category.name
    } for expense in valid_expenses])

    X = data['type']
    y = data['category']

    logger.info("Reentrenando modelo con datos reales...")

    accuracy = None
    if len(set(y)) > 1:
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            logger.info("Split: Train=%d, Test=%d", len(X_train), len(X_test))
            logger.info("Clases en test: %s", set(y_test))

            model = Pipeline([
                ('vectorizer', TfidfVectorizer()),
                ('classifier', MultinomialNB())
            ])
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info("Precisión del modelo (accuracy): %.2%%", accuracy)
        except Exception as e:
            logger.warning("Error calculando precisión: %s: %s", type(e).__name__, e)
            accuracy = None
    else:
        logger.warning("No hay suficientes categorías distintas para calcular el accuracy.")

    # Entrenamos con todos los datos (para producción)
    final_model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    final_model.fit(X, y)

    model_path = os.path.join(STATIC_ML_DIR, 'model.pkl')
    logger.info("STATIC_ML_DIR: %s", os.path.abspath(STATIC_ML_DIR))
    logger.info("Guardando modelo en %s...", model_path)
    joblib.dump(final_model, os.path.join(STATIC_ML_DIR, 'model.pkl'))

    logger.info("Modelo reentrenado con éxito usando %d registros.", len(y))

    category_counts = Counter(y)
    save_model_info(
        categories=sorted(list(set(y))),
        accuracy=round(accuracy * 100, 2) if accuracy is not None else None,
        sample_count=len(y),
        category_distribution=dict(category_counts)
    )


if __name__ == "__main__":
    retrain_model_from_db()
