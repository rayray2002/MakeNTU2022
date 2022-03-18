import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./C_SM.csv")

df["time"] = df["time"] - 1643587200

df["cum"] = df["instanceElectricity"].cumsum()
df["cum"] = df["cum"] * 60 / 1000 / 3600 + 6088.8

df.to_csv('test.csv')

df = df[["time", "normalUsage", "cum"]]
df.dropna().plot.line(x="time", figsize=(16, 8))
plt.show()
