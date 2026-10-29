"""Проверка сервиса предсказаний: те же запросы, что в примерах с curl.

Запуск:  python test_requests.py
Адрес сервиса можно переопределить:  python test_requests.py http://localhost:8001
"""
import json
import sys

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

CHECKS = [
    # (описание, метод, путь, тело или None, ожидаемый код)
    ("служебный адрес /health", "GET", "/health", None, 200),
    ("служебный адрес /ready", "GET", "/ready", None, 200),
    ("правильный запрос", "POST", "/predict",
     {"city": "moscow", "rooms": 2, "area": 54.5}, 200),
    ("нет поля area", "POST", "/predict",
     {"city": "moscow", "rooms": 2}, 422),
    ("строка вместо числа", "POST", "/predict",
     {"city": "moscow", "rooms": 2, "area": "54.5"}, 422),
    ("отрицательная площадь", "POST", "/predict",
     {"city": "moscow", "rooms": 2, "area": -1}, 422),
    ("незнакомый город", "POST", "/predict",
     {"city": "Москва", "rooms": 2, "area": 54.5}, 422),
]


def main() -> None:
    print(f"Сервис: {BASE}\n")
    failed = 0
    for title, method, path, body, expected in CHECKS:
        url = BASE + path
        try:
            if method == "GET":
                r = requests.get(url, timeout=5)
            else:
                # заголовок Content-Type: application/json библиотека ставит сама
                r = requests.post(url, json=body, timeout=5)
        except requests.ConnectionError:
            print(f"[  ошибка ] {title}: нет соединения с {url}")
            print("           Сервис запущен? Порт тот же? Внутри контейнера указан --host 0.0.0.0?")
            failed += 1
            continue

        ok = r.status_code == expected
        mark = "   ок    " if ok else " НЕ ТО   "
        print(f"[{mark}] {title}")
        print(f"           {method} {path}  ->  {r.status_code} (ожидали {expected})")
        try:
            print("           " + json.dumps(r.json(), ensure_ascii=False))
        except ValueError:
            print("           " + r.text[:200])
        print()
        if not ok:
            failed += 1

    if failed:
        print(f"Не прошло проверок: {failed} из {len(CHECKS)}")
        sys.exit(1)
    print(f"Все {len(CHECKS)} проверок прошли.")


if __name__ == "__main__":
    main()
