# Pricing Optimization Report

Portfolio weekly profit: **91,908 -> 96,517** (**+5.0%**) under constraints (±15% move, 12% margin floor).

## Elasticities

| product                  | category    |   elasticity_raw |    se |   ci_low |   ci_high |   n_weeks |   base_price |   unit_cost |   base_units |   elasticity |   true_e |
|:-------------------------|:------------|-----------------:|------:|---------:|----------:|----------:|-------------:|------------:|-------------:|-------------:|---------:|
| Aroma Diffuser           | home        |           -1.577 | 0.156 |   -1.887 |    -1.267 |       104 |       32     |        13.5 |        632   |       -1.459 |     -1.5 |
| Bluetooth Speaker Mini   | electronics |           -2.33  | 0.184 |   -2.695 |    -1.965 |       104 |       49     |        26   |        409   |       -2.273 |     -2.4 |
| Canvas Tote Bag          | accessories |           -2.953 | 0.178 |   -3.307 |    -2.599 |       104 |       12     |         3.8 |        864   |       -2.788 |     -2.8 |
| Ceramic Mug Set          | accessories |           -1.506 | 0.161 |   -1.826 |    -1.186 |       104 |       28     |        12   |        419   |       -1.665 |     -1.6 |
| Desk Plant Kit           | home        |           -0.93  | 0.178 |   -1.284 |    -0.577 |       104 |       16     |         6   |        496   |       -0.957 |     -1.2 |
| House Blend Coffee 1kg   | grocery     |           -2.564 | 0.194 |   -2.949 |    -2.178 |       104 |       14     |         7.5 |        292.5 |       -2.44  |     -2.6 |
| Organic Green Tea        | grocery     |           -1.284 | 0.163 |   -1.607 |    -0.96  |       104 |        9.5   |         4   |        622   |       -1.447 |     -1.4 |
| Premium Coffee Beans 1kg | grocery     |           -2.189 | 0.17  |   -2.526 |    -1.853 |       104 |       24     |        11   |        725.5 |       -2.15  |     -1.9 |
| Steel Water Bottle       | accessories |           -2.191 | 0.159 |   -2.506 |    -1.876 |       104 |       19     |         6.5 |        293   |       -2.196 |     -2.2 |
| USB-C Charging Hub       | electronics |           -1.772 | 0.162 |   -2.093 |    -1.45  |       104 |       39     |        17   |        624   |       -1.84  |     -1.8 |
| Weighted Blanket         | home        |           -0.641 | 0.184 |   -1.005 |    -0.277 |       104 |       76.135 |        38   |        248.5 |       -0.732 |     -0.9 |
| Wireless Earbuds Lite    | electronics |           -2.132 | 0.149 |   -2.427 |    -1.836 |       104 |       68.225 |        34   |        305   |       -2.119 |     -2.1 |

## Recommendations

| product                  | category    |   elasticity |   current_price |   recommended_price |   change_pct |   weekly_profit_now |   weekly_profit_new |   profit_uplift_pct | rationale                                     |
|:-------------------------|:------------|-------------:|----------------:|--------------------:|-------------:|--------------------:|--------------------:|--------------------:|:----------------------------------------------|
| Canvas Tote Bag          | accessories |       -2.788 |           12    |               10.2  |        -15   |                7085 |                8699 |                22.8 | unconstrained optimum 5.93 clamped to bounds  |
| Weighted Blanket         | home        |       -0.732 |           76.14 |               86.99 |         14.3 |                9477 |               11042 |                16.5 | inelastic (|e|<1): raise to constraint cap    |
| Steel Water Bottle       | accessories |       -2.196 |           19    |               16.15 |        -15   |                3662 |                4040 |                10.3 | unconstrained optimum 11.93 clamped to bounds |
| Desk Plant Kit           | home        |       -0.957 |           16    |               17.99 |         12.4 |                4960 |                5316 |                 7.2 | inelastic (|e|<1): raise to constraint cap    |
| Premium Coffee Beans 1kg | grocery     |       -2.15  |           24    |               20.4  |        -15   |                9432 |                9672 |                 2.5 | unconstrained optimum 20.57 within bounds     |
| Aroma Diffuser           | home        |       -1.459 |           32    |               35.99 |         12.5 |               11692 |               11974 |                 2.4 | unconstrained optimum 42.91 clamped to bounds |
| Organic Green Tea        | grocery     |       -1.447 |            9.5  |                9.99 |          5.2 |                3421 |                3464 |                 1.3 | unconstrained optimum 12.95 clamped to bounds |
| House Blend Coffee 1kg   | grocery     |       -2.44  |           14    |               11.99 |        -14.4 |                1901 |                1917 |                 0.8 | unconstrained optimum 12.71 within bounds     |
| Wireless Earbuds Lite    | electronics |       -2.119 |           68.22 |               63.99 |         -6.2 |               10439 |               10477 |                 0.4 | unconstrained optimum 64.38 within bounds     |
| Bluetooth Speaker Mini   | electronics |       -2.273 |           49    |               45.99 |         -6.1 |                9407 |                9443 |                 0.4 | unconstrained optimum 46.42 within bounds     |
| Ceramic Mug Set          | accessories |       -1.665 |           28    |               29.99 |          7.1 |                6704 |                6724 |                 0.3 | unconstrained optimum 30.05 within bounds     |
| USB-C Charging Hub       | electronics |       -1.84  |           39    |               36.99 |         -5.2 |               13728 |               13749 |                 0.2 | unconstrained optimum 37.24 within bounds     |

## Scenario projection

| product                  |   price |   units_proj |   revenue_now |   revenue_proj |   profit_now |   profit_proj |
|:-------------------------|--------:|-------------:|--------------:|---------------:|-------------:|--------------:|
| Aroma Diffuser           |   35.99 |          532 |         20224 |          19162 |        11692 |         11974 |
| Bluetooth Speaker Mini   |   45.99 |          472 |         20041 |          21725 |         9407 |          9443 |
| Canvas Tote Bag          |   10.2  |         1359 |         10368 |          13864 |         7085 |          8699 |
| Ceramic Mug Set          |   29.99 |          374 |         11732 |          11208 |         6704 |          6724 |
| Desk Plant Kit           |   17.99 |          443 |          7936 |           7976 |         4960 |          5316 |
| House Blend Coffee 1kg   |   11.99 |          427 |          4095 |           5119 |         1901 |          1917 |
| Organic Green Tea        |    9.99 |          578 |          5909 |           5778 |         3421 |          3464 |
| Premium Coffee Beans 1kg |   20.4  |         1029 |         17412 |          20990 |         9432 |          9672 |
| Steel Water Bottle       |   16.15 |          419 |          5567 |           6761 |         3662 |          4040 |
| USB-C Charging Hub       |   36.99 |          688 |         24336 |          25442 |        13728 |         13749 |
| Weighted Blanket         |   86.99 |          225 |         18920 |          19608 |         9477 |         11042 |
| Wireless Earbuds Lite    |   63.99 |          349 |         20809 |          22356 |        10439 |         10477 |
| TOTAL                    |  nan    |         6895 |        167349 |         179989 |        91908 |         96517 |
