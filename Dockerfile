# --- Stage 1: Builder ---
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ /app/scripts/

ARG MODEL_VERSION=v0.1
RUN python scripts/train.py --version ${MODEL_VERSION}

# --- Stage 2: Final Image ---
FROM python:3.10-slim
WORKDIR /app
RUN useradd -m appuser
USER appuser

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

ARG MODEL_VERSION=v0.1
COPY --from=builder /app/models/model-${MODEL_VERSION}.joblib /app/models/
COPY --from=builder /app/models/metrics-${MODEL_VERSION}.json /app/models/
COPY app/ /app/app/

EXPOSE 8000
ENV MODEL_VERSION=${MODEL_VERSION}

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]