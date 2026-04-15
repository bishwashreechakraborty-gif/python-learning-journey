import pandas as pd
import os

# Get current file directory
base_path = os.path.dirname(__file__)

# Join path
file_path = os.path.join(base_path, "data.csv")

df = pd.read_csv(file_path)

print(df.head())