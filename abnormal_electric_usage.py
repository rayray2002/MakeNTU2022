import numpy as np
import pandas as pd

abnormal = False
users = ["A", "B", "C", "D", "E", "F"]
user = users[0]

t_start_index = 0
t_end_index = 1000
df = pd.read_csv(f"data/{user}_SM.csv")
IEdataList = df["instanceElectricity"][t_start_index: t_end_index]
newIEDataList = df["instanceElectricity"][t_start_index: t_end_index]

r_IE = np.corrcoef(IEdataList, newIEDataList)[0, 1]

print(r_IE)

if r_IE < 0.7:
    abnormal = True
    print("abnormal instance electricity usage")
