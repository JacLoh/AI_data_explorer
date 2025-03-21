# utils/file_handler.py

import pandas as pd

def parse_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)
