"""Dynamic Pricing Optimizer — task-runner.

Run named tasks directly:
    python tasks.py demo          # full end-to-end pipeline
    python tasks.py estimate      # elasticity estimation only (needs output/sales_history.csv)
    python tasks.py optimize      # price optimization (needs output/sales_history.csv)
    python tasks.py help          # list all tasks

Pattern: strategy/policy objects behind a task-runner harness.
Each task name maps to a function; no argparse, no subcommands — just
plain Python called by name from the command line.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dpo.datagen import generate_sales, true_elasticities
from dpo.elasticity import estimate_elasticities
from dpo.optimizer import Constraints, recommend_prices, simulate

OUT = Path(__file__).parent / "output"


# ── helpers ───────────────────────────────────────────────────────────────────

def _chart(rec: pd.DataFrame) -> None:
    r = rec.sort_values("profit_uplift_pct")
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#cc3311" if v < 0 else "#228833" for v in r["profit_uplift_pct"]]
    ax.barh(r["product"], r["profit_uplift_pct"], color=colors)
    ax.set_xlabel("projected weekly profit uplift (%)")
    ax.set_title("Recommended price moves — profit impact")
    fig.tight_layout()
    fig.savefig(OUT / "pricing_impact.png", dpi=110)
    plt.close(fig)


def _load_sales() -> pd.DataFrame:
    p = OUT / "sales_history.csv"
    if not p.exists():
        print(f"  sales_history.csv not found — run  python tasks.py demo  first")
        sys.exit(1)
    return pd.read_csv(p)


# ── tasks ─────────────────────────────────────────────────────────────────────

def task_demo() -> None:
    """Full pipeline: generate → estimate elasticities → optimize → report."""
    OUT.mkdir(exist_ok=True)
    print("TASK demo / step 1: generating 2-year weekly sales (12 products) …")
    df = generate_sales(seed=42)
    df.to_csv(OUT / "sales_history.csv", index=False)

    print("TASK demo / step 2: estimating elasticities …")
    est = estimate_elasticities(df)
    truth = true_elasticities()
    est["true_e"] = est["product"].map(truth)
    err = (est["elasticity"] - est["true_e"]).abs().mean()
    print(est[["product", "elasticity", "ci_low", "ci_high", "true_e"]].to_string(index=False))
    print(f"  mean |estimated − true| = {err:.3f}")

    print("TASK demo / step 3: optimizing prices (±15%, margin ≥12%) …")
    rec = recommend_prices(est)
    print(rec[["product", "current_price", "recommended_price", "change_pct",
               "profit_uplift_pct", "rationale"]].to_string(index=False))

    print("TASK demo / step 4: writing report + chart …")
    _chart(rec)
    sim = simulate(est, dict(zip(rec["product"], rec["recommended_price"])))
    total = sim[sim["product"] == "TOTAL"].iloc[0]
    uplift = (total["profit_proj"] / total["profit_now"] - 1) * 100
    lines = [
        "# Pricing Optimization Report", "",
        f"Portfolio weekly profit uplift: **{uplift:+.1f}%** "
        f"(±15% cap, 12% margin floor).", "",
        "## Elasticities", "", est.round(3).to_markdown(index=False), "",
        "## Recommendations", "", rec.to_markdown(index=False), "",
        "## Scenario projection", "", sim.to_markdown(index=False), "",
    ]
    (OUT / "pricing_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Weekly profit uplift: {uplift:+.1f}%  →  {OUT / 'pricing_report.md'}")


def task_estimate() -> None:
    """Re-estimate elasticities from the saved sales history."""
    df = _load_sales()
    print(estimate_elasticities(df).to_string(index=False))


def task_optimize() -> None:
    """Re-run price optimization from the saved sales history."""
    df = _load_sales()
    est = estimate_elasticities(df)
    rec = recommend_prices(est)
    print(rec[["product", "current_price", "recommended_price",
               "change_pct", "profit_uplift_pct"]].to_string(index=False))


def task_help() -> None:
    """List available tasks."""
    print("Available tasks:")
    for name, fn in TASKS.items():
        doc = (fn.__doc__ or "").strip().splitlines()[0]
        print(f"  {name:<12}  {doc}")


TASKS: dict[str, object] = {
    "demo":     task_demo,
    "estimate": task_estimate,
    "optimize": task_optimize,
    "help":     task_help,
}

if __name__ == "__main__":
    task_name = sys.argv[1] if len(sys.argv) > 1 else "help"
    if task_name not in TASKS:
        print(f"Unknown task: {task_name!r}. Run  python tasks.py help")
        sys.exit(1)
    TASKS[task_name]()
