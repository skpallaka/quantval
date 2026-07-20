# fetch.py
import yfinance as yf
import pandas as pd
from cache import init_db, save_to_cache, load_from_cache, is_range_cached, log_fetch

def get_price_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    init_db()

    if is_range_cached(ticker, start, end):
        df = load_from_cache(ticker, start, end)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        df = df.drop(columns=["ticker"])
    else:
        df = yf.download(ticker, start=start, end=end)
        df.dropna(inplace=True)
        df.columns = df.columns.get_level_values(0)
        save_to_cache(df, ticker)
        log_fetch(ticker, start, end)

    df.columns = [c.lower() for c in df.columns]  # normalize regardless of path
    df = df[["open", "high", "low", "close", "volume"]]  # enforce consistent column order
    return df


if __name__ == "__main__":
    df = get_price_data("AAPL", "2015-01-01", "2024-01-01")
    print(df.shape)
    print(df.head())
    print("NaN count:", df.isna().sum().sum())