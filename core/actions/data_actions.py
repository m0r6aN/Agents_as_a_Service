# core/actions/data_actions.py

import pandas as pd

def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "missing_data": df.isnull().sum().to_dict(),
    }