import pandas as pd

df = pd.read_excel("profile_data.xlsx", sheet_name="positions_rows")
print(df.columns.tolist())
