"""Пакетное применение модели: без сервиса и без HTTP.

Скрипт сам загружает модель, читает объявления из CSV, считает цену для каждого
и пишет результат в файл. Так работает batch-режим с лекции.

Запуск:  python batch_score.py sample.csv
Результат: predictions_batch.csv
"""
import csv
import pickle
import sys

from train import make_features

MODEL_PATH = "model.bin"


def main(path: str) -> None:
    with open(MODEL_PATH, "rb") as f:
        dv, model = pickle.load(f)          # один раз, как и в сервисе

    scored = 0
    errors: dict = {}

    with open(path, newline="", encoding="utf-8") as src, \
         open("predictions_batch.csv", "w", newline="", encoding="utf-8") as dst:
        writer = csv.writer(dst)
        writer.writerow(["row", "status", "price", "error"])

        for i, row in enumerate(csv.DictReader(src)):
            # Приведение типов: строка, которая не превращается в число, это ошибка.
            try:
                listing = {"city": row["city"], "rooms": int(row["rooms"]), "area": float(row["area"])}
            except ValueError as e:
                errors["type"] = errors.get("type", 0) + 1
                writer.writerow([i, "type", "", str(e)[:120]])
                continue

            # TODO (необязательно). Здесь нет проверки диапазонов и списка городов.
            #   Площадь 545 и город «Москва» дойдут до модели и получат цену.
            #   Подключите схему Listing из app.py:
            #       from app import Listing
            #       from pydantic import ValidationError
            #   и проверяйте каждую строку через Listing.model_validate(listing),
            #   ловя ValidationError как ошибку "schema". Сравните число ошибок
            #   с тем, что даёт сервис через batch_client.py.

            X = dv.transform([make_features(listing)])
            price = round(float(model.predict(X)[0]))
            writer.writerow([i, "ok", price, ""])
            scored += 1

    print(f"всего: {scored + sum(errors.values())}, оценено: {scored}, ошибок: {errors}")
    print("результаты: predictions_batch.csv")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample.csv")
