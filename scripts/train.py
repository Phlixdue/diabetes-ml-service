import argparse
import json
import os
from joblib import dump

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Constants
RANDOM_STATE = 42
MODEL_DIR = "models"

def train(model_version="v0.1"):
    """Trains a model and saves it with its metrics."""
    print(f"🚀 Starting training for version: {model_version}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    Xy = load_diabetes(as_frame=True)
    X, y = Xy.frame.drop(columns=["target"]), Xy.frame["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    if model_version == "v0.1":
        print("Training baseline LinearRegression model.")
        model = LinearRegression()
    elif model_version == "v0.2":
        print("Training improved Ridge model.")
        model = Ridge(alpha=1.0, random_state=RANDOM_STATE)
    else:
        raise ValueError("Unknown model version")

    pipeline = Pipeline(steps=[("preprocessor", StandardScaler()), ("regressor", model)])
    pipeline.fit(X_train, y_train)
    print("✅ Training complete.")

    y_pred = pipeline.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"📊 Test RMSE: {rmse:.2f}")

    model_path = os.path.join(MODEL_DIR, f"model-{model_version}.joblib")
    metrics_path = os.path.join(MODEL_DIR, f"metrics-{model_version}.json")

    dump(pipeline, model_path)
    print(f"✅ Model saved to {model_path}")

    with open(metrics_path, "w") as f:
        json.dump({"rmse": rmse}, f)
    print(f"✅ Metrics saved to {metrics_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", type=str, default="v0.1", help="Model version to train (e.g., v0.1, v0.2)"
    )
    args = parser.parse_args()
    train(model_version=args.version)