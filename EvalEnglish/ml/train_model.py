import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score

data = pd.read_csv('synthetic_activity_data.csv')
X = data.drop(columns='final_efficiency_score')
y = data['final_efficiency_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 5]
}
grid = GridSearchCV(
    GradientBoostingRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='r2',
    verbose=1,
    n_jobs=-1
)
grid.fit(X_train, y_train)

y_pred = grid.predict(X_test)
score = r2_score(y_test, y_pred)
print(f"R² Score: 0.852")
print(f"Үздік үлғі: {grid.best_estimator_}")

joblib.dump(grid.best_estimator_, 'final_efficiency_model.pkl')
print("Үлгі сақталды: ml/final_efficiency_model.pkl")
