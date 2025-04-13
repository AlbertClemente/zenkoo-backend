import json
import os

def get_model_info():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_ml_path = os.path.join(base_dir, '..', 'static', 'ml', 'model_info.json')

    if not os.path.exists(static_ml_path):
        return {
            "lastTrainedAt": None,
            "sampleCount": 0,
            "categories": [],
            "accuracy": None,
            "modelVersion": None,
            "categoryDistribution": {}
        }

    with open(static_ml_path, "r") as f:
        return json.load(f)