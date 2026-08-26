FROM python:3.13-slim

WORKDIR /app/src


COPY . .

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["python", "main.py"]