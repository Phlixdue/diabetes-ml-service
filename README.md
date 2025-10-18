**Virtual Diabetes Clinic ML Service**

This project is a small, containerized machine learning service that predicts a diabetes progression index. It's designed to help a virtual clinic prioritize patient follow-ups by providing a continuous risk score. The entire CI/CD and release process is automated using GitHub Actions.

This repository fulfills an MLOps assignment by demonstrating a reproducible, versioned, and automated pipeline for an ML service.

Key Features
Prediction API: A POST /predict endpoint that returns a diabetes progression score.

Health Check: A GET /health endpoint to monitor service status and model version.

Versioned Models: The service is released with version tags (e.g., v0.1, v0.2), each using a different model.

Containerized: Packaged as a self-contained Docker image for portability.

Automated CI/CD: Workflows for linting, testing, building, and publishing releases to the GitHub Container Registry (GHCR).

**Running the Service with Docker**

docker pull ghcr.io/phlixdue/diabetes-ml-service:v0.1
docker pull ghcr.io/phlixdue/diabetes-ml-service:v0.2