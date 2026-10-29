FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY model.bin .

# TODO 1. Осмысленная версия: дата и имя модели, например 2026-11-05-linreg
ENV MODEL_VERSION=TODO

EXPOSE 8000

# TODO 2. Порт, тот же, что при локальном запуске
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "TODO"]
