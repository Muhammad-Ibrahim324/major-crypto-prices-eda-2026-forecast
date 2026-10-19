# Forecast and results file guide

Author: Muhammad Ibrahim Shahrukh.

## crypto_forecasts_2026.csv

370 rows: 74 daily forecast dates for each of five symbols. These are predictions, not observations. Origin is the last completed historical date.

| Column | Short description | Meaning |
|---|---|---|
| date | Forecast calendar date | Future daily date, including weekends. |
| symbol | Cryptocurrency trading symbol | BTC, ETH, USDT, BNB or XRP. |
| ticker | Yahoo Finance ticker | USD ticker identifier. |
| forecast_origin | Last observed calendar date | Information cutoff for the prediction. |
| horizon_days | Days after forecast origin | 1 through 74. |
| selected_model | Validation selected model | Selected using mean validation WAPE only. |
| forecast_close_usd | Predicted closing price | Positive USD estimate. |
| lower_illustrative_band_usd | Illustrative lower price bound | Heuristic validation-error band; not guaranteed coverage. |
| upper_illustrative_band_usd | Illustrative upper price bound | Heuristic validation-error band; not guaranteed coverage. |

`year_end_projection.csv` keeps only December 31 rows and adds the latest observed close and projected percentage change relative to it.

## Evaluation outputs

| File | Interpretation |
|---|---|
| chronological_splits.csv | Validation/test origin dates and future windows. |
| validation_metrics.csv | MAE, RMSE, WAPE and sMAPE by asset, model and fold. |
| model_leaderboard.csv | Mean validation WAPE, its fold standard deviation, mean MAE and selected flag. |
| test_metrics.csv | Once-only held-out evaluation of the selected candidate and last-price comparator. |
| test_predictions.csv | Actual and predicted held-out paths, baseline and illustrative bands. |
| feature_importance.csv | Selected fitted-model importance; absent when no learned model wins. |
| historical_summary.csv | Returns, volatility, drawdowns, tails and volume summaries over each asset's available history. |
| coverage.csv | Start/end dates, counts, zero-volume days and internal calendar gaps. |
| analysis_summary.md | Generated interpretation grounded in the computed results. |
| environment.json | Key execution environment versions. |
| execution_report.json | Notebook execution method, code counts and plot counts. |

`mae_usd` is mean absolute error. `rmse_usd` is root mean squared error. `wape_pct = 100 × sum(abs(error)) / sum(abs(actual))`. `smape_pct = 200 × mean(abs(error) / (abs(actual) + abs(prediction)))`. Both use all days in a fixed-origin path.

`mae_skill_vs_last_price = 1 − selected_model_MAE / last_price_MAE`; positive is better, negative worse. `illustrative_band_test_coverage_pct` is the fraction of held-out actual closes within the validation-derived band. `usdt_mae_bps_of_peg = 10,000 × USDT MAE in USD`. That final field applies only to USDT, so it is blank for the other coins.

Volatility annualization uses sqrt(365). Drawdowns use each asset's own running historical maximum. Cross-asset return correlations and normalized performance charts use a common observed date range. Full-history volatility comparisons have different lookback lengths for BTC and the other four assets.

## Exclusions

`excluded_observations.csv` retains the same nine raw-derived fields as the historical CSV plus `exclusion_reason`. Multiple reasons are separated by semicolons. Five rows are excluded in this snapshot; all are potentially incomplete October 19 candles, and BNB additionally violates OHLC bounds.
