import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from joblib import load
from .schemas import DiabetesFeatures

MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.1")
MODEL_PATH = f"models/model-{MODEL_VERSION}.joblib"

app = FastAPI(title="Diabetes Prediction API", version=MODEL_VERSION)

try:
    model = load(MODEL_PATH)
except FileNotFoundError:
    model = None

@app.on_event("startup")
async def startup_event():
    if model:
        print(f"✅ Model {MODEL_VERSION} loaded.")
    else:
        print(f"❌ Model file not found at {MODEL_PATH}")

@app.get("/health")
def read_health():
    return {"status": "ok", "model_version": MODEL_VERSION}

@app.post("/predict")
def predict(features: DiabetesFeatures):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    feature_df = pd.DataFrame([features.model_dump()])
    try:
        prediction = model.predict(feature_df)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")