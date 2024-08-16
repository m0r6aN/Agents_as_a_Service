# core/tools/data_processing.py

import numpy as np

def detect_outliers(data, threshold=3):
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold