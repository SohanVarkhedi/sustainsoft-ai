import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib
import os

DATA_PATH = "data/logs/sustainsoft_dataset.csv"
MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "sustainsoft_regressor.joblib")

def main():
    df = pd.read_csv(DATA_PATH)

    # Features and target
    X = df[["cpu_usage", "ram_usage_mb", "process_count", "disk_io_mb"]]
    y = df["sustainability_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Model trained.")
    print("MAE:", round(mae, 3))
    print("Saved to:", MODEL_PATH)

if __name__ == "__main__":
    main()