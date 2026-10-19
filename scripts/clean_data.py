"""Clean the supplied yfinance MultiIndex CSV without inventing prices."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pandas as pd

def clean(source, destination, snapshot_date="2026-10-19"):
    source, destination = Path(source), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(source, header=[0, 1], index_col=0)
    expected = {"BTC-USD", "ETH-USD", "USDT-USD", "BNB-USD", "XRP-USD"}
    assert set(raw.columns.get_level_values(0)) == expected
    parts, empty_rows = [], 0
    for ticker in sorted(expected):
        block = raw[ticker].copy()
        empty_rows += int(block.isna().all(axis=1).sum())
        block = block.dropna(how="all")
        block.columns = [c.lower().replace(" ", "_") for c in block.columns]
        block.index = pd.to_datetime(block.index, errors="raise")
        block.index.name = "date"
        block = block.reset_index()
        block.insert(1, "symbol", ticker.split("-")[0])
        block.insert(2, "ticker", ticker)
        parts.append(block)
    data = pd.concat(parts, ignore_index=True)
    cols = ["date", "symbol", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    data = data[cols]
    numeric = cols[3:]
    data[numeric] = data[numeric].apply(pd.to_numeric, errors="raise")
    duplicate_count = int(data.duplicated().sum())
    data = data.drop_duplicates().copy()
    if data.duplicated(["date", "ticker"]).any():
        raise ValueError("Conflicting date/ticker duplicates require manual review.")
    reasons = pd.Series("", index=data.index)
    def flag(mask, reason):
        reasons.loc[mask] += reason + ";"
    flag(data.date >= pd.Timestamp(snapshot_date), "potentially_incomplete_daily_candle")
    flag(~np.isfinite(data[numeric]).all(axis=1), "missing_or_nonfinite_value")
    flag((data[["open","high","low","close","adj_close"]] <= 0).any(axis=1), "nonpositive_price")
    flag((data.volume < 0) | (data.volume % 1 != 0), "invalid_volume")
    flag((data.high < data[["open","close","low"]].max(axis=1)) |
         (data.low > data[["open","close","high"]].min(axis=1)), "inconsistent_ohlc")
    audit = data.loc[reasons.ne("")].copy()
    audit["exclusion_reason"] = reasons[reasons.ne("")].str.rstrip(";")
    data = data.loc[reasons.eq("")].sort_values(["date","ticker"]).reset_index(drop=True)
    data.volume = data.volume.astype("int64")
    assert not data.isna().any().any()
    gaps = {}
    for ticker, group in data.groupby("ticker"):
        missing = pd.date_range(group.date.min(), group.date.max()).difference(group.date)
        gaps[ticker] = [str(d.date()) for d in missing]
    report = {
        "source_file": source.name, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "snapshot_date": snapshot_date, "raw_calendar_rows": len(raw),
        "empty_precoverage_asset_rows_removed": empty_rows,
        "exact_duplicate_rows_removed": duplicate_count, "excluded_observations": len(audit),
        "clean_observations": len(data), "first_date": str(data.date.min().date()),
        "last_date": str(data.date.max().date()), "missing_calendar_dates": gaps,
        "adj_close_equals_close": bool(np.array_equal(data.adj_close, data.close)),
        "note": "User-reported yfinance provenance; no independent historical re-download."
    }
    data.to_csv(destination/"major_crypto_daily_clean.csv", index=False, date_format="%Y-%m-%d")
    audit.to_csv(destination/"excluded_observations.csv", index=False, date_format="%Y-%m-%d")
    (destination/"quality_report.json").write_text(json.dumps(report, indent=2))
    return data, audit, report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--output", default="data")
    parser.add_argument("--snapshot-date", default="2026-10-19")
    args = parser.parse_args()
    _, _, report = clean(args.source, args.output, args.snapshot_date)
    print(json.dumps(report, indent=2))
