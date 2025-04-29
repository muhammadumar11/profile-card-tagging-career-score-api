import pandas as pd

xls = pd.ExcelFile("profile_data.xlsx")
print(xls.sheet_names)
