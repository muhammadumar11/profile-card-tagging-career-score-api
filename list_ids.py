import pandas as pd

df = pd.read_excel("profile_data.xlsx", sheet_name="profiles_rows")
print(df["id"].head(3))
