"""Optional new collection recipe; not the unknown original download command."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, hashlib
import pandas as pd
import yfinance as yf

parser=argparse.ArgumentParser()
parser.add_argument("--snapshot-date",default="2026-10-19")
parser.add_argument("--output",default="data/raw/major_crypto_refreshed.csv")
args=parser.parse_args()
settings=dict(tickers=["BTC-USD","ETH-USD","USDT-USD","BNB-USD","XRP-USD"],
              start="2014-09-17",end=args.snapshot_date,interval="1d",group_by="ticker",
              auto_adjust=False,repair=False,rounding=False,actions=False,threads=False,
              progress=False,multi_level_index=True)
data=yf.download(**settings)
if data is None or data.empty: raise RuntimeError("No data returned.")
expected=set(settings["tickers"])
if set(data.columns.get_level_values(0)) != expected: raise RuntimeError("Missing ticker response.")
for ticker in sorted(expected):
    if data[ticker]["Close"].dropna().empty: raise RuntimeError(f"Empty series: {ticker}")
out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
if out.exists(): raise FileExistsError("Choose a new output filename to preserve existing snapshots.")
data.to_csv(out)
metadata={"downloaded_at_utc":datetime.now(timezone.utc).isoformat(),"yfinance_version":yf.__version__,
          "settings":settings,"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
          "note":"New collection; provider revisions may differ from earlier snapshots. End date is exclusive."}
out.with_suffix(".metadata.json").write_text(json.dumps(metadata,indent=2))
print(f"Saved {len(data)} calendar rows to {out}.")
