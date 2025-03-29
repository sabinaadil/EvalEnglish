import joblib
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'final_efficiency_model.pkl')


def evaluate_final_efficiency_score(metrics: dict) -> float:
    model = joblib.load(MODEL_PATH)
    efficiency_per_minute = metrics['average_score'] / metrics['time_spent'] if metrics['time_spent'] > 0 else 0
    correct_ratio = metrics['average_score'] / metrics['avg_attempts'] if metrics['avg_attempts'] > 0 else 0
    teacher_model_gap = abs(metrics['average_teacher_score'] - metrics['average_model_score'])
    late_ratio = metrics['late_submissions'] / metrics['tasks_completed'] if metrics['tasks_completed'] > 0 else 0
    X = np.array([[
        metrics['tasks_completed'],
        metrics['average_score'],
        metrics['average_teacher_score'],
        metrics['average_model_score'],
        metrics['time_spent'],
        metrics['avg_attempts'],
        metrics['late_submissions'],
        efficiency_per_minute,
        correct_ratio,
        teacher_model_gap,
        late_ratio
    ]])
    prediction = model.predict(X)[0]
    return round(prediction, 2)


