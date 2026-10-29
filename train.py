"""Обучение модели оценки стоимости квартиры по объявлению.

Данные синтетические, чтобы занятие не зависело от сети.
Запуск:  python train.py
Результат: файл model.bin, внутри кортеж (преобразователь признаков, модель).
"""
import pickle

import numpy as np
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

SEED = 42
N_ROWS = 2000
CITIES = ["moscow", "spb", "kazan", "ekb"]
PRICE_PER_SQM = {"moscow": 300_000, "spb": 200_000, "kazan": 120_000, "ekb": 110_000}


def generate_listings(n: int, rng: np.random.Generator) -> list[dict]:
    """Объявления: город, число комнат, площадь и цена."""
    rows = []
    for _ in range(n):
        city = rng.choice(CITIES)
        rooms = int(rng.integers(1, 6))                       # 1..5 комнат
        area = round(float(18 + rooms * 16 + rng.normal(0, 8)), 1)
        area = max(area, 15.0)
        price = PRICE_PER_SQM[city] * area * (1 + 0.03 * rooms)
        price *= rng.normal(1.0, 0.08)                         # шум рынка
        rows.append({"city": city, "rooms": rooms, "area": area, "price": round(price)})
    return rows


def make_features(row: dict) -> dict:
    """Та же сборка признаков, что в сервисе. Менять только вместе."""
    return {"city_rooms": f"{row['city']}_{row['rooms']}", "area": row["area"]}


def main() -> None:
    rng = np.random.default_rng(SEED)
    rows = generate_listings(N_ROWS, rng)

    split = int(len(rows) * 0.8)
    train_rows, val_rows = rows[:split], rows[split:]

    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform([make_features(r) for r in train_rows])
    y_train = [r["price"] for r in train_rows]

    model = LinearRegression()
    model.fit(X_train, y_train)

    X_val = dv.transform([make_features(r) for r in val_rows])
    y_val = [r["price"] for r in val_rows]
    mae = mean_absolute_error(y_val, model.predict(X_val))

    with open("model.bin", "wb") as f:
        pickle.dump((dv, model), f)

    print(f"rows: {len(rows)}, cities: {', '.join(CITIES)}")
    print(f"validation MAE: {mae:,.0f} rub".replace(",", " "))
    print(f"scikit-learn {sklearn.__version__}")
    print("saved: model.bin")


if __name__ == "__main__":
    main()
