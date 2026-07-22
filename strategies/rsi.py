import pandas as pd
import numpy as np

def generate_signals(close: pd.Series) -> pd.Series:
    change = close.diff()
    gains = change.where(change > 0, other = 0)
    losses = (-change).where(change < 0, other = 0)
    avg_gain = gains.rolling(window=14).mean()
    avg_loss = losses.rolling(window=14).mean()
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))


    raw_sig = pd.Series(np.nan,index=close.index)
    raw_sig[rsi < 30] = 1
    raw_sig[rsi > 70] = 0
    sig = raw_sig.ffill()
    return sig
