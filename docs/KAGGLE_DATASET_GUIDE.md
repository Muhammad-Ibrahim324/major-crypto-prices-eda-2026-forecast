# Kaggle publishing guide

Author: **Muhammad Ibrahim Shahrukh**

## Copy-ready metadata

**Dataset title (46 / 50 characters):** Crypto Historical Prices: BTC ETH USDT BNB XRP

**Subtitle (80 / 80 characters):** Daily USD prices, volume, EDA and 2026 forecasts for five major cryptocurrencies

**Notebook title (35 / 50 characters):** Crypto Prices: EDA & 2026 Forecasts

Suggested tags: cryptocurrency, bitcoin, ethereum, finance, time series, exploratory data analysis, forecasting, machine learning.

## Dataset description

Explore daily historical cryptocurrency prices for **Bitcoin (BTC), Ethereum (ETH), Tether (USDT), BNB and XRP**, quoted in US dollars. This beginner-friendly dataset contains **17,479 observations** with open, high, low, close, adjusted close and provider-reported trading volume in one tidy CSV. Bitcoin coverage begins on **September 17, 2014**; the other four assets begin on **November 9, 2017**. Completed observations end on **October 18, 2026**.

The supplied Yahoo Finance/yfinance export was reshaped from multi-level columns into a simple one-row-per-asset-per-day table. Empty pre-coverage blocks were removed, column names standardized, duplicate keys and OHLC bounds checked, and potentially incomplete October 19 candles excluded. An audit preserves every excluded observation. No prices were fabricated, interpolated, forward filled or rounded for presentation.

Use the data to learn pandas, build candlestick dashboards, compare normalized price performance, study volatility and drawdowns, investigate return correlations and USDT peg deviations, or develop chronological forecasting experiments. The companion notebook includes colorful Plotly charts, a static dashboard, baseline and machine-learning comparisons, an untouched test period, and separate daily projections through December 31, 2026.

**Author:** Muhammad Ibrahim Shahrukh. **Source:** user-reported Yahoo Finance data collected with yfinance; original download settings and timestamp were not supplied. These are cryptocurrency prices, not equity prices. Forecasts are experimental estimates and are not observed market data or investment advice.

## Coverage

| symbol | ticker | start | end | rows |
|---|---|---|---|---|
| BNB | BNB-USD | 2017-11-09 | 2026-10-18 | 3266 |
| BTC | BTC-USD | 2014-09-17 | 2026-10-18 | 4415 |
| ETH | ETH-USD | 2017-11-09 | 2026-10-18 | 3266 |
| USDT | USDT-USD | 2017-11-09 | 2026-10-18 | 3266 |
| XRP | XRP-USD | 2017-11-09 | 2026-10-18 | 3266 |

## Column descriptions

The short-description column contains 1–5 words per field and can be copied into Kaggle's column descriptions.

| Column | Short description | Type or unit | Meaning |
|---|---|---|---|
| date | Observation calendar date | YYYY-MM-DD | Source daily date label; no timezone in CSV. |
| symbol | Cryptocurrency trading symbol | Text | BTC, ETH, USDT, BNB or XRP. |
| ticker | Yahoo Finance ticker | Text | Provider identifier, e.g. BTC-USD. |
| open | Daily opening price | USD | Provider-reported opening price. |
| high | Daily highest price | USD | Provider-reported daily high. |
| low | Daily lowest price | USD | Provider-reported daily low. |
| close | Daily closing price | USD | Observed close, not a forecast. |
| adj_close | Provider adjusted closing price | USD | Equals close in this snapshot; kept for traceability. |
| volume | Provider reported trading volume | Integer | Preserved Yahoo value; not assumed to be a count of coins. |

## Short file description

`major_crypto_daily_clean.csv` contains 17,479 daily observations for BTC-USD, ETH-USD, USDT-USD, BNB-USD and XRP-USD, sorted by date and ticker. Its nine columns hold the date, asset identifiers, USD OHLC prices, adjusted close and original provider-reported volume. The covered period is September 17, 2014–October 18, 2026, with shorter histories for four assets. The file has no missing values, duplicate date/ticker keys or calendar gaps inside an asset's available history. Potentially incomplete October 19 rows and the inconsistent BNB observation are preserved separately in the exclusions file. No forecast values are mixed into this historical CSV.

## Provenance and collection methodology

The input is the user-supplied `major_crypto.csv`, reported to originate from Yahoo Finance using yfinance. It contains two header rows (`Ticker`, `Price`) and a date index. Each ticker has Open, High, Low, Close, Adj Close and Volume fields. The raw file spans 4,416 calendar dates and ends October 19, 2026. The original retrieval code, yfinance version, request parameters and exact timestamp are unknown. A two-level header and Adj Close are consistent with a multi-ticker export, but do not prove the original settings. No independent historical download was made during this preparation.

The original file is preserved under `data/raw/`. Its SHA-256 is `d829f2dffb8d330e04beca6190727c51c62ab68ac63b7642361f4db61930f77c`. Source dates are retained without adding an unsupported timezone. Coverage starts do not necessarily correspond to token launches. Yahoo's underlying contributors and historical aggregation methods are not independently verified for this file. Reported volume is retained without relabeling it as shares, coins or independently verified exchange activity.

### Exact transformation record

1. Read the ticker and price header levels, retaining the first actual observation (September 17, 2014).
2. Create one long-format table per ticker and concatenate them.
3. Remove 4,596 fully empty asset/date slots before available coverage. These are not observations and are not filled.
4. Standardize to nine lowercase snake_case columns; parse dates and numeric fields.
5. Remove exact duplicate rows if present (none found). Conflicting duplicate keys trigger an error rather than silently keeping one.
6. Validate finite positive prices, nonnegative integer volume, unique keys and high/low bounds.
7. Exclude all five rows dated October 19 because that day was still underway at preparation. BNB additionally fails OHLC validation: close 732.0 exceeds high 729.7835083007812. One BNB row has two reasons, not two separate excluded observations.
8. Preserve excluded values and reasons in `excluded_observations.csv`; retain 17,479 clean observations through October 18.
9. Retain Adj Close, which exactly matches Close here; retain numeric precision and integer volume. Sort by date, then ticker.
10. Confirm no nulls, no conflicting duplicates and no missing daily dates within each retained asset's history. No outlier clipping, imputation, resampling or conversion is applied to the published historical CSV.

### Repeatable collection example

`scripts/download_data.py` supplies a documented **new collection recipe**, not a claim about the original command. It explicitly sets five USD tickers, daily interval, ticker grouping, `auto_adjust=False`, `repair=False`, and `rounding=False`, and records the collection timestamp and library version. yfinance's end date is exclusive. Provider revisions mean a later download may not match this snapshot byte-for-byte. The collector needs internet access and is not required to run the notebook.

### Updating the snapshot

Keep old versions. Download to a new filename, set the cleaner's `--snapshot-date` to the collection date, inspect exclusions, and update the notebook's `SNAPSHOT_DATE` and forecast end when needed. The collector defaults to dates strictly before its snapshot date, avoiding a partial current-day candle. The cleaner can also accept the supplied file containing the partial day. Re-run all cells; never append predictions to the observation table.

## Beginner quick start

```python
import pandas as pd
df = pd.read_csv("major_crypto_daily_clean.csv", parse_dates=["date"])
btc = df.loc[df["symbol"].eq("BTC")].sort_values("date")
btc["daily_return"] = btc["close"].pct_change(fill_method=None)
print(btc.tail())
```

Use group-wise return calculations when processing all five assets. A plain `df.close.pct_change()` on interleaved tickers produces invalid cross-asset returns. Align comparison start dates. Treat USDT as a stablecoin and include weekends in crypto forecasts.

## Notebook methodology

The notebook covers schema and quality checks, coverage, full-history summary statistics, normalized prices, candlesticks, moving averages, volume, returns, rolling volatility, drawdowns, tail distributions, return correlations, monthly heatmaps, weekday exploration and USDT deviations. Exploratory calendar patterns are not presented as trading signals.

Forecast targets are cumulative log returns at each horizon from day 1 to day 74. Features include lagged returns, rolling momentum/volatility, distance from moving averages, intraday range, open-to-close change, relative volume, weekday encodings and USDT peg deviation. Training uses up to four recent years and excludes any training row whose final target occurs after the forecast origin. No recursive future-volume assumptions are needed.

Candidates are Last price, Recent drift, Ridge alpha 100, Ridge alpha 1000, and Extra Trees (100 trees, maximum depth 10, minimum leaf 20). USDT also gets a Dollar peg baseline. Three sequential non-overlapping validation windows rank candidates by mean WAPE. The final 74-day block is held out until model selection is complete. The final fit then uses all eligible completed history. This is the best validation model among tested candidates, not a universal best-model claim.

MAE and RMSE are in USD; WAPE and sMAPE are percentages. Held-out MAE skill is `1 − model MAE / last-price MAE`; a negative value means the selected model lost to the baseline. USDT MAE is also reported in basis points of its $1 peg. The model does not forecast trading profitability.

Illustrative uncertainty bands use the 90th percentile of validation absolute log errors normalized by square-root horizon. Dependence within forecast paths, three validation regimes and changing volatility limit reliability. These are not guaranteed 90% prediction intervals. Held-out coverage is reported without recalibration on the test data.

## Upload instructions

1. Create the Kaggle dataset using the title, subtitle and description above.
2. Upload `data/major_crypto_daily_clean.csv`. Optionally include the exclusions CSV, quality JSON and this guide.
3. Keep forecast CSVs separate and explicitly label them as predictions if you publish them.
4. Import `crypto_eda_2026_forecasts.ipynb`, attach the dataset, and run all cells. The loader discovers the clean filename beneath `/kaggle/input` and deduplicates identical paths.
5. Review the notebook's executed output, write a short notebook introduction, and add source links and your author credit.
6. Select a dataset license only after checking your rights to redistribute the underlying data. No open-data license is inferred from yfinance's software license.

## Short answers for dataset discovery

**What does this cryptocurrency dataset contain?** Daily USD OHLC prices, adjusted close and provider-reported volume for BTC, ETH, USDT, BNB and XRP.

**What is the date range?** September 17, 2014–October 18, 2026 overall; four assets start November 9, 2017.

**Is it suitable for beginners?** Yes. The tidy CSV, short data dictionary and documented notebook show how to load, inspect, visualize and evaluate it.

**Does it include forecasts?** The historical CSV contains observations only. Companion result files contain experimental daily forecasts through December 31, 2026.

**Are stablecoin prices handled differently?** Yes. USDT has peg-deviation analysis and a $1 baseline in the model comparison.

**Is the data independently verified?** No. It is an audited transformation of the user-supplied snapshot, with user-reported yfinance provenance.

## Sources and suggested citation

- [Yahoo Finance BTC-USD historical data](https://finance.yahoo.com/quote/BTC-USD/history/)
- [Yahoo Finance ETH-USD historical data](https://finance.yahoo.com/quote/ETH-USD/history/)
- [Yahoo Finance USDT-USD historical data](https://finance.yahoo.com/quote/USDT-USD/history/)
- [Yahoo Finance BNB-USD historical data](https://finance.yahoo.com/quote/BNB-USD/history/)
- [Yahoo Finance XRP-USD historical data](https://finance.yahoo.com/quote/XRP-USD/history/)
- [yfinance project and data-use notice](https://github.com/ranaroussi/yfinance)
- [yfinance download API](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html)
- [scikit-learn time-series cross-validation guidance](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- [Plotly renderer documentation](https://plotly.com/python/renderers/)

Suggested citation: Muhammad Ibrahim Shahrukh (2026), *Crypto Historical Prices: BTC ETH USDT BNB XRP*. Yahoo Finance/yfinance user-supplied snapshot, cleaned completed data through October 18, 2026. Add the published Kaggle URL and version number after upload.
