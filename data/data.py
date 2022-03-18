import pandas as pd
import os
from functools import reduce


dataList = pd.read_excel("raw/Available Device _ Scope.xlsx")[["資料項目", "Scope"]]

users = ["A", "B", "C", "D", "E"]
devices = ["PV", "SM", "AC", "ESS", "EV Charger"]

for user in users:
    dfs = []
    for device in devices:
        if not os.path.isfile(f"raw/{user}用戶_{device}.xlsm"):
            continue
        print(device)

        df = pd.read_excel(f"raw/{user}用戶_{device}.xlsm")
        df = df.astype({"timestamp": int, "value": float})

        df = df.pivot_table(
            index="timestamp", columns="scope", values="value", aggfunc="mean"
        )
        df.rename(columns=dict(zip(dataList["資料項目"], dataList["Scope"])), inplace=True)
        
        # print(df)
        df.to_csv(f"{user}_{device}.csv")
        dfs.append(df)

    print(dfs)
    out = reduce(lambda df1, df2: pd.merge(df1, df2, on="timestamp", how="outer"), dfs)
    out = out.sort_values(by=['timestamp'])
    out.to_csv(f"{user}_out.csv")
    print(out)
