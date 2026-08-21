"""Synthetic weekly sales history with known price elasticities per product."""
from __future__ import annotations

import numpy as np
import pandas as pd

CATALOG = [
    # (product, category, base_price, unit_cost, true_elasticity)
    ("Premium Coffee Beans 1kg", "grocery", 24.0, 11.0, -1.9),
    ("House Blend Coffee 1kg", "grocery", 14.0, 7.5, -2.6),
    ("Organic Green Tea", "grocery", 9.5, 4.0, -1.4),
    ("Steel Water Bottle", "accessories", 19.0, 6.5, -2.2),
    ("Canvas Tote Bag", "accessories", 12.0, 3.8, -2.8),
    ("Ceramic Mug Set", "accessories", 28.0, 12.0, -1.6),
    ("Bluetooth Speaker Mini", "electronics", 49.0, 26.0, -2.4),
    ("USB-C Charging Hub", "electronics", 39.0, 17.0, -1.8),
    ("Wireless Earbuds Lite", "electronics", 69.0, 34.0, -2.1),
    ("Desk Plant Kit", "home", 16.0, 6.0, -1.2),
    ("Aroma Diffuser", "home", 32.0, 13.5, -1.5),
    ("Weighted Blanket", "home", 79.0, 38.0, -0.9),
]


def generate_sales(weeks: int = 104, seed: int = 42) -> pd.DataFrame:
    """Weekly rows: week, product, category, price, unit_cost, promo, units_sold."""
    rng = np.random.default_rng(seed)
    rows = []
    for name, cat, base_p, cost, elast in CATALOG:
        base_demand = rng.uniform(180, 900)
        for w in range(weeks):
            promo = int(rng.random() < 0.12)
            price = base_p * float(rng.choice([0.85, 0.9, 0.95, 1.0, 1.0, 1.05, 1.1, 1.15]))
            if promo:
                price = round(price * 0.85, 2)
            season = 0.18 * np.sin(2 * np.pi * (w % 52) / 52)
            ln_q = (np.log(base_demand) + elast * np.log(price / base_p)
                    + season + 0.35 * promo + rng.normal(0, 0.16))
            rows.append({"week": w, "product": name, "category": cat,
                         "price": round(price, 2), "unit_cost": cost, "promo": promo,
                         "units_sold": int(np.exp(ln_q))})
    return pd.DataFrame(rows)


def true_elasticities() -> dict[str, float]:
    return {name: e for name, _, _, _, e in CATALOG}
