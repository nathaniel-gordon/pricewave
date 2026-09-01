# PriceWave — Dynamic Pricing Engine with Elasticity Modeling & Constrained Optimization

PriceWave is a production-grade pricing engine that estimates own-price demand elasticity from historical transactions, applies hierarchical category shrinkage to stabilize noisy estimates, and solves constrained profit-maximization problems behind a backtest harness.

## Mathematical Formulation

1. **Log-Log Demand Elasticity**:
   $$\ln(Q_i) = lpha_i + eta_i \ln(P_i) + \gamma X_i + \epsilon_i$$
   Where $eta_i$ is the price elasticity of demand for product $i$.
2. **Hierarchical Shrinkage**: Blends SKU-level elasticity with category and department priors using Empirical Bayes to prevent overfitting on low-volume items.
3. **Constrained Profit Optimization**:
   $$\max_{\{P_i\}} \sum_{i} (P_i - C_i) \cdot Q_i(P_i) \quad 	ext{s.t.} \quad P_{\min, i} \le P_i \le P_{\max, i}, \quad \left|rac{P_i - P_{0, i}}{P_{0, i}}ight| \le \delta$$

## Usage

```bash
# Run elasticity estimation and pricing optimization simulation
python tasks.py run-backtest
```

## Tests

```bash
pytest tests/ -v
```
