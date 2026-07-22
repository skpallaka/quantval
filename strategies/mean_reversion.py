import pandas as pd 
import numpy as np

def generate_signals(close):
    r_mean = close.rolling(window=20).mean()
    r_std = close.rolling(window=20).std()
    z_score = (close - r_mean) / r_std 
    signal = (z_score < -2).astype(float)
    signal = signal.where(z_score.notna(), other=np.nan)
    return signal 