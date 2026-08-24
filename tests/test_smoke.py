"""Smoke test: python tests/test_smoke.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dpo.datagen import generate_sales, true_elasticities
from dpo.elasticity import estimate_elasticities
from dpo.optimizer import Constraints, optimal_price, recommend_prices, simulate


def main() -> None:
    df = generate_sales(weeks=104, seed=3)
    est = estimate_elasticities(df)
    truth = true_elasticities()
    err = (est["elasticity"] - est["product"].map(truth)).abs()
    assert err.mean() < 0.35, f"elasticity recovery too weak: mean err {err.mean():.3f}"
    assert (est["ci_low"] < est["elasticity_raw"]).all()
    assert (est["ci_high"] > est["elasticity_raw"]).all()

    assert optimal_price(-2.0, 10.0) == 20.0          # p* = c*e/(1+e)
    assert optimal_price(-0.5, 10.0) is None          # inelastic

    rec = recommend_prices(est, Constraints())
    assert (rec["change_pct"].abs() <= 15.01).all(), "constraint violated"
    m = rec.merge(est[["product", "unit_cost"]], on="product")
    assert (m["recommended_price"] >= m["unit_cost"] * 1.119).all(), "margin floor violated"
    assert rec["profit_uplift_pct"].mean() > 0, "recommendations should raise profit on average"

    sim = simulate(est, dict(zip(rec["product"], rec["recommended_price"])))
    total = sim[sim["product"] == "TOTAL"].iloc[0]
    assert total["profit_proj"] > total["profit_now"]
    print(f"OK - elasticity err={err.mean():.3f}, portfolio profit "
          f"{total['profit_now']:.0f} -> {total['profit_proj']:.0f}")


if __name__ == "__main__":
    main()


def test_smoke():
    main()
