import pandas as pd
import numpy as np

def generate_signals(close:pd.Series) -> pd.Series:
    change = close.diff(periods=90)
    signal = (change > 0).astype(float)
    signal = signal.where(change.notna(), other=np.nan)
    return signal

