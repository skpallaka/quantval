from data.fetch import get_price_data
from strategies.momentum import generate_signals

df = get_price_data("AAPL", "2015-01-01","2024-01-01")
signal = generate_signals(df["close"])
print(signal.head(95))
print("\nSignal value counts:")
print(signal.value_counts(dropna=False))