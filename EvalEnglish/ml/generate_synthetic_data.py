import pandas as pd
import numpy as np

def generate_synthetic_dataset(n=1000, save_path='synthetic_activity_data.csv'):
    np.random.seed(42)
    data = {
        'tasks_completed': np.random.randint(1, 21, size=n),
        'average_score': np.round(np.random.normal(0.7, 0.1, size=n).clip(0, 1), 2),
        'average_teacher_score': np.round(np.random.normal(0.65, 0.12, size=n).clip(0, 1), 2),
        'average_model_score': np.round(np.random.normal(0.7, 0.15, size=n).clip(0, 1), 2),
        'time_spent': np.random.randint(60, 1000, size=n),
        'avg_attempts': np.round(np.random.normal(1.5, 0.7, size=n).clip(1, 5), 2),
        'late_submissions': np.random.poisson(1.0, size=n).clip(0, 5)
    }
    df = pd.DataFrame(data)
    df['efficiency_per_minute'] = np.round(df['average_score'] / df['time_spent'], 5)
    df['correct_ratio'] = np.round(df['average_score'] / df['avg_attempts'], 4)
    df['teacher_model_gap'] = np.round(abs(df['average_teacher_score'] - df['average_model_score']), 3)
    df['late_ratio'] = np.round(df['late_submissions'] / df['tasks_completed'], 4)
    df['final_efficiency_score'] = np.round(
        5
        + df['tasks_completed'] * 0.1
        + df['average_score'] * 2
        + df['average_teacher_score'] * 1.5
        + df['average_model_score'] * 1.5
        - df['avg_attempts'] * 0.5
        - df['late_submissions'] * 0.3
        + df['correct_ratio'] * 0.8
        - df['teacher_model_gap'] * 0.6
        + np.random.normal(0, 0.4, size=n),
        2
    )
    df['final_efficiency_score'] = np.clip(df['final_efficiency_score'], 1, 10)
    df.to_csv(save_path, index=False)
    print(f"Синтетикалық деректер жинағы сақталды: {save_path}")

if __name__ == '__main__':
    generate_synthetic_dataset(n=1000)
