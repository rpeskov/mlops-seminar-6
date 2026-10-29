"""Сервис оценки стоимости квартиры. Заготовка с четырьмя пропусками.

Пропуски помечены словом TODO. Заполняйте сверху вниз.
Запуск:  uvicorn app:app --host 0.0.0.0 --port 8000
"""
import logging
import os
import pickle
import time
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, ConfigDict, Field

MODEL_PATH = os.getenv("MODEL_PATH", "model.bin")
MODEL_VERSION = os.getenv("MODEL_VERSION", "dev")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("price-estimate")


# ---------- схемы запроса и ответа ----------

class Listing(BaseModel):
    """Объявление, по которому оцениваем цену."""
    model_config = ConfigDict(extra="forbid", strict=True)

    # TODO 1. Три поля с ограничениями:
    #   city  -- один из четырёх городов: moscow, spb, kazan, ekb. Тип Literal[...]
    #   rooms -- целое число от 1 до 6.        Field(ge=..., le=...)
    #   area  -- дробное число, больше 10 и не больше 500.   Field(gt=..., le=...)
    ...


class PriceEstimate(BaseModel):
    price: float
    model_version: str


# ---------- состояние сервиса ----------

STATE: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO 2. Загрузить модель один раз при старте.
    #   Открыть MODEL_PATH в бинарном режиме, прочитать через pickle кортеж (dv, model),
    #   положить в STATE под ключами "dv" и "model". Всё до строки yield.
    ...
    log.info("model %s loaded from %s", MODEL_VERSION, MODEL_PATH)
    yield
    STATE.clear()


app = FastAPI(title="price-estimate", lifespan=lifespan)

# ---------- метрики для занятия 8, сегодня не трогаем ----------

PREDICTIONS = Counter("predictions_total", "Сколько предсказаний сделано", ["model_version"])
LATENCY = Histogram("prediction_latency_seconds", "Время одного предсказания")


@app.get("/metrics", include_in_schema=False)
def metrics():
    """Счётчики в текстовом формате Prometheus."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---------- журналирование запросов, заготовка для домашнего задания ----------

@app.middleware("http")
async def access_log(request: Request, call_next):
    response = await call_next(request)
    # Домашнее задание: добавить время обработки и запись ошибок.
    log.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response


# ---------- адреса ----------

@app.get("/health")
def health():
    """Процесс жив."""
    return {"status": "ok"}


@app.get("/ready")
def ready():
    """Модель загружена, можно слать запросы."""
    # TODO 3. Если в STATE нет ключа "model", вернуть 503 через HTTPException
    #   с detail="model not loaded". Иначе вернуть словарь со status="ready"
    #   и model_version=MODEL_VERSION.
    return {"status": "TODO 3 не заполнен"}


@app.post("/predict", response_model=PriceEstimate)
def predict(listing: Listing):
    # TODO 4. Собрать признаки так же, как в train.py (функция make_features):
    #   {"city_rooms": "<город>_<комнаты>", "area": <площадь>}
    #   Прогнать через STATE["dv"].transform([...]) и STATE["model"].predict(...),
    #   взять первый элемент, превратить в float. Вернуть PriceEstimate с
    #   price=round(y) и model_version=MODEL_VERSION.
    raise HTTPException(status_code=501, detail="TODO 4 не заполнен")
