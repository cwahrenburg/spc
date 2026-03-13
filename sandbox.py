import pandas as pd
from config import DB
from helpers import cs50_query_to_df

# # Select all measurements
# qry = f"SELECT * FROM measurements"

# df0 = cs50_query_to_df(DB=DB, qry=qry)
# print(df0["feature_id"].unique())

# for featureID in df0["feature_id"].unique(): 
#     print(df1.query("feature_id == @featureID"))

data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data, index = [5, 6, 7])

print(df["Name"].iloc)