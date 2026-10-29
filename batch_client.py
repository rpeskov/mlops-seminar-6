"""Пакетный клиент: отправляет объявления из CSV в сервис и считает статистику.

Запуск:  python batch_client.py sample.csv
Домашнее задание: заполнить два TODO.
"""
import csv
import sys
import time

import requests

URL = "http://localhost:8000/predict"


def to_payload(row: dict) -> dict:
    """Строка CSV в тело запроса. Приведение типов намеренно простое:
    если значение не приводится, оставляем как есть и пусть сервис решает."""
    payload = {"city": row["city"]}
    try:
        payload["rooms"] = int(row["rooms"])
    except ValueError:
        payload["rooms"] = row["rooms"]
    try:
        payload["area"] = float(row["area"])
    except ValueError:
        payload["area"] = row["area"]
    return payload


def main(path: str) -> None:
    ok = 0
    errors: dict = {}          # код ответа -> сколько раз
    durations: list[float] = []

    with requests.Session() as session, \
         open(path, newline="", encoding="utf-8") as src, \
         open("predictions.csv", "w", newline="", encoding="utf-8") as dst:
        writer = csv.writer(dst)
        writer.writerow(["row", "status", "price", "model_version", "error"])

        for i, row in enumerate(csv.DictReader(src)):
            payload = to_payload(row)
            started = time.perf_counter()

            # TODO 1. Отправить POST-запрос с payload в URL через session.
            #   Поймать requests.RequestException: записать строку с status="network"
            #   и перейти к следующей.
            ...

            durations.append(time.perf_counter() - started)

            # TODO 2. Если код 200: ok += 1, записать price и model_version из ответа.
            #   Иначе: увеличить errors[код], записать код и первые 200 символов тела.
            ...

    total = ok + sum(errors.values())
    avg_ms = sum(durations) / len(durations) * 1000 if durations else 0
    print(f"всего: {total}, успешно: {ok}, ошибок: {errors}")
    print(f"среднее время ответа: {avg_ms:.1f} мс")
    print("результаты: predictions.csv")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample.csv")
