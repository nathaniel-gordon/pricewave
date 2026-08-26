# PriceWave — Dynamic Pricing Optimization Engine

> Set prices that maximize profit, not just match competitors. PriceWave estimates own-price elasticity per product from sales history using log-log OLS with hierarchical shrinkage, then solves for profit-maximizing prices under business constraints and projects portfolio-level revenue impact.

## What PriceWave Does

- **Elasticity estimation** — log-log OLS controlling for promotions and seasonality per product
- **Hierarchical shrinkage** — regularizes noisy item-level estimates toward category means
- **Constrained optimization** — profit maximization under floor/ceiling and margin constraints
- **Portfolio impact projection** — revenue, margin, and volume delta across the full assortment
- **Scenario comparison** — compare current vs optimized vs competitor-matched pricing

## Architecture

```
Sales History (product x date x price x quantity)
    └─> ElasticityEstimator  (log-log OLS + hierarchical shrinkage)
    └─> ConstraintEngine     (floor/ceiling, margin guard)
    └─> ProfitOptimizer      (per-product optimal price solver)
    └─> PortfolioProjector   (revenue / margin / volume delta)
    └─> TaskRunner           (tasks.py demo / compare / report)
```

## Quickstart

```bash
python tasks.py demo        # estimate elasticities + optimize prices on synthetic data
python tasks.py report      # generate portfolio pricing report
```

## Test

```bash
python tests/test_smoke.py
```

---

## 👤 Author & Contact

- **Author**: Nathaniel Gordon
- **Role**: Senior AI & Machine Learning Engineer
- **GitHub**: [github.com/nathaniel-gordon](https://github.com/nathaniel-gordon)
- **Portfolio / Upwork**: [upwork.com/freelancers/~015fe5a704f8943797](https://www.upwork.com/freelancers/~015fe5a704f8943797)
- **Email**: nathanielgordon346@gmail.com
- **Location**: Tallahassee, FL, USA
