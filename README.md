<div align="center">

# 🏷️ PriceWave

**Maximal-profit pricing with empirical elasticity curves and margin guardrails.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-22c55e?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![Domain](https://img.shields.io/badge/Domain-Pricing%20Science%20%2F%20Economics-10b981?style=for-the-badge)](https://github.com/nathaniel-gordon/pricewave)

<br/>

*Dynamic price optimization (DPO) and econometric elasticity modeling engine. Estimates constant and variable price elasticity from historical transaction logs, solves for closed-form unconstrained profit optima, and applies business constraint bounding with charm pricing.*

</div>

---

## 🧠 What Is This?

> **For non-technical readers:** When a business wants to change the price of a product, how do they know if raising the price by $5 will boost profit or cause customers to stop buying? PriceWave looks at historical sales and price changes to calculate *price sensitivity* (elasticity) for every item in your catalog. It then computes the exact price that maximizes total revenue or profit — while respecting business safety guardrails (like never selling below cost and limiting maximum price swings to ±15%).

---

## 🏗️ Architecture & Mathematical Foundation

PriceWave implements econometric demand modeling and constrained optimization in a two-stage pipeline: **Elasticity Estimation** followed by **Constrained Closed-Form Profit Maximization**.

```
📊 Historical Orders & Price Variation Data
                    │
                    ▼
📈 Log-Log Econometric Regression (OLS / WLS)
   ln(Quantity) = α + ϵ · ln(Price) + β · Covariates + u
                    │
                    ▼
🎯 Elasticity Regime Categorization
   ├── Inelastic (|ϵ| < 1.0) ──► Pricing Power (Raise to Constraint Bound)
   ├── Unit Elastic (|ϵ| = 1.0) ──► Revenue Neutral
   └── Elastic (|ϵ| > 1.0) ──► Sensitive (Solve Closed-Form Optimum)
                    │
                    ▼
⚙️ Constrained Optimization Engine
   ├── Closed-Form Optimal Price:  p* = (c · ϵ) / (1 + ϵ)
   ├── Min Margin Floor:  p_min = Unit Cost × (1 + Margin Target)
   ├── Max Change Bounding:  [p₀ × (1 - Δ_max), p₀ × (1 + Δ_max)]
   └── Psychological Charm Pricing:  p → ⌊p⌋ - 0.01  (e.g., $49.99)
                    │
                    ▼
📋 Recommended Price Roster + Scenario Simulation Matrix
```

---

## 🔬 Econometric & Optimization Formulations

### 1. Constant-Elasticity Demand Formulation
Demand $Q(p)$ is modeled under the constant elasticity of demand assumption:

$$Q(p) = A \cdot p^{\epsilon}$$

Where:
- $p$ is the unit price.
- $\epsilon = \frac{dQ/Q}{dp/p} < 0$ is the price elasticity of demand.
- $A > 0$ is the baseline demand scale parameter.

### 2. Closed-Form Profit Maximization
Given unit production cost $c > 0$, total profit $\Pi(p)$ is:

$$\Pi(p) = (p - c) \cdot Q(p) = (p - c) \cdot A p^{\epsilon}$$

Taking the first derivative $\frac{d\Pi}{dp}$ and setting to zero:

$$\frac{d\Pi}{dp} = A p^{\epsilon} + (p - c) \cdot \epsilon A p^{\epsilon - 1} = 0$$

$$p + \epsilon(p - c) = 0 \implies p(1 + \epsilon) = \epsilon c$$

$$p^* = \frac{c \cdot \epsilon}{1 + \epsilon} \quad \text{for } \epsilon < -1$$

### 3. Boundary & Guardrail Conditions
When $|\epsilon| \le 1.0$ (inelastic demand), the unconstrained mathematical optimum diverges to $+\infty$. PriceWave automatically activates boundary enforcement:

$$p_{\text{rec}} = \min\left(p_0 \cdot (1 + \Delta_{\text{max}}), \max\left(p_0 \cdot (1 - \Delta_{\text{max}}), c \cdot (1 + \text{Margin}_{\text{min}}), p^*\right)\right)$$

---

## 📊 Feature & Constraint Capabilities

| Dimension | Implementation | Description |
|---|---|---|
| 📉 **Elasticity Fit** | `dpo.elasticity` | Robust log-log OLS with outlier filtering & R² validation |
| 🛡️ **Margin Floors** | `Constraints.min_margin_pct` | Enforces minimum gross margin hurdle per product category |
| 🔄 **Volatility Dampening** | `Constraints.max_change_pct` | Limits price delta to prevent customer sticker shock (e.g. ±15%) |
| 🏷️ **Charm Pricing** | `dpo.optimizer._charm` | Rounds calculated optima to `.99` endings for psychological conversion |
| 🧪 **Scenario Simulation** | `dpo.optimizer` | Simulates revenue and profit deltas under competitor response scenarios |

---

## 🚀 Getting Started

```bash
git clone https://github.com/nathaniel-gordon/pricewave
cd pricewave
pip install -e .
```

### Run Elasticity Estimation & Price Optimization

```bash
# Run the synthetic dataset generation and price optimization pipeline
python -m dpo.optimizer
```

### Python API Example

```python
import pandas as pd
from dpo.optimizer import Constraints, recommend_prices

# Load product elasticity estimates
estimates = pd.DataFrame([
    {"sku": "SKU-101", "base_price": 24.99, "unit_cost": 10.00, "elasticity": -1.85, "base_units": 1200},
    {"sku": "SKU-202", "base_price": 89.00, "unit_cost": 50.00, "elasticity": -0.65, "base_units": 450},
])

constraints = Constraints(
    max_change_pct=15.0,
    min_margin_pct=20.0,
    charm_pricing=True
)

recommendations = recommend_prices(estimates, constraints)
print(recommendations[["sku", "base_price", "recommended_price", "expected_profit_delta_pct"]])
```

### Run Tests

```bash
pytest tests/ -v
```

---

## 📁 Project Structure

```
pricewave/
├── dpo/
│   ├── datagen.py          # Synthetic e-commerce transaction generator
│   ├── elasticity.py       # Log-log econometric regression & elasticity solver
│   ├── optimizer.py        # Constrained profit maximization & charm pricing
│   └── __init__.py
├── tasks.py                # Automation & benchmark task runner
└── tests/
    └── test_smoke.py       # Optimization invariants & margin unit tests
```

---

<div align="center">

*Built by [Nathaniel Gordon](https://github.com/nathaniel-gordon)*

</div>
