from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "model_version" in response.json()

def test_predict_success():
    payload = {
        "age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03,
        "s1": -0.02, "s2": 0.03, "s3": -0.02, "s4": 0.02,
        "s5": 0.02, "s6": -0.001
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)

def test_predict_bad_input():
    # Missing 's6' feature
    payload = { "age": 0.02, "sex": -0.044, "bmi": 0.06 }
    response = client.post("/predict", json=payload)
    # FastAPI's Pydantic validation returns 422
    assert response.status_code == 422