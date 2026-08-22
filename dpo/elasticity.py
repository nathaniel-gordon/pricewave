"""Elasticity estimation: per-product log-log OLS with hierarchical shrinkage."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def estimate_elasticities(df: pd.DataFrame, shrink_k: float = 30.0) -> pd.DataFrame:
    """ln(units) ~ ln(price) + promo + season terms, per product.

    Shrinkage: e_final = w * e_product + (1-w) * e_category,  w = n / (n + shrink_k).
    Partial pooling stabilizes products with short or low-variation price history.
    """
    rows = []
    for (product, category), g in df.groupby(["product", "category"]):
        g = g[(g["units_sold"] > 0) & (g["price"] > 0)]
        ln_q = np.log(g["units_sold"].to_numpy(dtype=float))
        ln_p = np.log(g["price"].to_numpy(dtype=float))
        season_sin = np.sin(2 * np.pi * (g["week"] % 52) / 52)
        season_cos = np.cos(2 * np.pi * (g["week"] % 52) / 52)
        X = np.column_stack([np.ones(len(g)), ln_p, g["promo"].to_numpy(dtype=float),
                             season_sin, season_cos])
        beta, res, *_ = np.linalg.lstsq(X, ln_q, rcond=None)
        resid = ln_q - X @ beta
        dof = max(len(g) - X.shape[1], 1)
        sigma2 = float(resid @ resid) / dof
        cov = sigma2 * np.linalg.inv(X.T @ X)
        se = float(np.sqrt(cov[1, 1]))
        t975 = stats.t.ppf(0.975, dof)
        rows.append({"product": product, "category": category,
                     "elasticity_raw": float(beta[1]), "se": se,
                     "ci_low": float(beta[1] - t975 * se),
                     "ci_high": float(beta[1] + t975 * se),
                     "n_weeks": len(g),
                     "base_price": float(g["price"].median()),
                     "unit_cost": float(g["unit_cost"].iloc[0]),
                     "base_units": float(g[g["promo"] == 0]["units_sold"].median())})
    est = pd.DataFrame(rows)
    cat_mean = est.groupby("category")["elasticity_raw"].transform("mean")
    w = est["n_weeks"] / (est["n_weeks"] + shrink_k)
    est["elasticity"] = (w * est["elasticity_raw"] + (1 - w) * cat_mean).round(3)
    for c in ("elasticity_raw", "se", "ci_low", "ci_high", "base_price", "base_units"):
        est[c] = est[c].round(3)
    return est
