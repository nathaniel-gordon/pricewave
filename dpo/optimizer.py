"""Constrained profit-maximizing price recommendations + scenario simulation."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Constraints:
    max_change_pct: float = 15.0     # max move from current price
    min_margin_pct: float = 12.0     # price must exceed cost by this margin
    charm_pricing: bool = True       # round to .99 endings


def optimal_price(elasticity: float, unit_cost: float) -> float | None:
    """Constant-elasticity closed form: p* = c * e / (1 + e), valid for e < -1."""
    if elasticity >= -1.0:
        return None  # inelastic: unconstrained optimum unbounded, defer to constraint cap
    return unit_cost * elasticity / (1.0 + elasticity)


def _charm(p: float) -> float:
    return max(np.floor(p) - 0.01, 0.99) if p >= 1 else round(p, 2)


def recommend_prices(est: pd.DataFrame, cons: Constraints | None = None) -> pd.DataFrame:
    cons = cons or Constraints()
    rows = []
    for _, r in est.iterrows():
        p0, c, e, q0 = r["base_price"], r["unit_cost"], r["elasticity"], r["base_units"]
        lo = max(p0 * (1 - cons.max_change_pct / 100), c * (1 + cons.min_margin_pct / 100))
        hi = p0 * (1 + cons.max_change_pct / 100)
        star = optimal_price(e, c)
        if star is None:
            p_new = hi  # inelastic -> push to cap
            rationale = "inelastic (|e|<1): raise to constraint cap"
        else:
            p_new = float(np.clip(star, lo, hi))
            rationale = (f"unconstrained optimum {star:.2f} "
                         + ("within" if lo <= star <= hi else "clamped to") + " bounds")
        if cons.charm_pricing:
            p_new = _charm(p_new)
            p_new = float(np.clip(p_new, lo, hi)) if p_new < lo or p_new > hi else p_new
        q_new = q0 * (p_new / p0) ** e
        profit0 = (p0 - c) * q0
        profit1 = (p_new - c) * q_new
        rows.append({"product": r["product"], "category": r["category"],
                     "elasticity": e, "current_price": round(p0, 2),
                     "recommended_price": round(p_new, 2),
                     "change_pct": round((p_new / p0 - 1) * 100, 1),
                     "weekly_profit_now": round(profit0, 0),
                     "weekly_profit_new": round(profit1, 0),
                     "profit_uplift_pct": round((profit1 / profit0 - 1) * 100, 1)
                     if profit0 > 0 else float("nan"),
                     "rationale": rationale})
    out = pd.DataFrame(rows)
    return out.sort_values("profit_uplift_pct", ascending=False).reset_index(drop=True)


def simulate(est: pd.DataFrame, price_overrides: dict[str, float]) -> pd.DataFrame:
    """Project weekly revenue/profit for a proposed price vector vs current."""
    rows = []
    for _, r in est.iterrows():
        p0, c, e, q0 = r["base_price"], r["unit_cost"], r["elasticity"], r["base_units"]
        p1 = float(price_overrides.get(r["product"], p0))
        q1 = q0 * (p1 / p0) ** e
        rows.append({"product": r["product"], "price": round(p1, 2),
                     "units_proj": round(q1, 0),
                     "revenue_now": round(p0 * q0, 0), "revenue_proj": round(p1 * q1, 0),
                     "profit_now": round((p0 - c) * q0, 0),
                     "profit_proj": round((p1 - c) * q1, 0)})
    out = pd.DataFrame(rows)
    total = {"product": "TOTAL", "price": np.nan,
             "units_proj": out["units_proj"].sum(),
             "revenue_now": out["revenue_now"].sum(), "revenue_proj": out["revenue_proj"].sum(),
             "profit_now": out["profit_now"].sum(), "profit_proj": out["profit_proj"].sum()}
    return pd.concat([out, pd.DataFrame([total])], ignore_index=True)
