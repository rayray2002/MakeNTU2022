import pandas as pd
import os
from functools import reduce


dataList = pd.read_excel("raw/Available Device _ Scope.xlsx")[["資料項目", "Scope"]]

users = ["A", "B", "C", "D", "E"]
device = 'SM'

for user in users:
    if not os.path.isfile(f"raw/{user}用戶_{device}.xlsm"):
        continue
    print(user)

    df = pd.read_excel(f"raw/{user}用戶_{device}.xlsm")
    df = df.astype({"timestamp": int, "value": float})

    df = df.pivot_table(
        index="timestamp", columns="scope", values="value", aggfunc="mean"
    )
    df.rename(columns=dict(zip(dataList["資料項目"], dataList["Scope"])), inplace=True)
    
    df = df.reindex(range(df.index.min(), df.index.max()+1))
    df = df.sort_index()

    df = df.interpolate(method='linear')
    df.to_csv(f"{user}_{device}.csv")
