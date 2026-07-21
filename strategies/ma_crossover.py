import pandas as pd
import numpy as np

def generate_signals(close: pd.Series) -> pd.Series:
    fast_ma = close.rolling(window=20).mean()
    slow_ma = close.rolling(window=50).mean()
    signal= (fast_ma > slow_ma).astype(float)
    signal = signal.where(slow_ma.notna(),other= np.nan)
    return signal
