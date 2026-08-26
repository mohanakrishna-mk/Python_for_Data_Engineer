FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

WORKDIR /app/src

# One async worker per pod.
# Scale pods horizontally with Kubernetes/HPA.
CMD ["python", "av-scan-svc.py"]
