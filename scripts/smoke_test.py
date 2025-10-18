import os
import requests
import sys

BASE_URL = "http://localhost:8000"
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.1")

def run_smoke_test():
    """Runs checks to ensure the containerized API is operational."""
    print("--- Running Smoke Test ---")
    
    # 1. Test Health Check
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        health = response.json()
        assert health["status"] == "ok"
        assert health["model_version"] == MODEL_VERSION
        print(f"✅ Health check passed for version {health['model_version']}.")
    except Exception as e:
        print(f"❌ Health check FAILED: {e}")
        sys.exit(1)

    # 2. Test Prediction
    payload = {
        "age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03, "s1": -0.02,
        "s2": 0.03, "s3": -0.02, "s4": 0.02, "s5": 0.02, "s6": -0.001
    }
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        response.raise_for_status()
        assert "prediction" in response.json()
        print("✅ Prediction endpoint passed.")
    except Exception as e:
        print(f"❌ Prediction endpoint FAILED: {e}")
        sys.exit(1)

    print("--- Smoke Test Successful ---")
    sys.exit(0)

if __name__ == "__main__":
    run_smoke_test()