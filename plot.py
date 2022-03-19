import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', 500)

users = ["A", "B", "C", "D", "E", "F"]
for user in users:
    df = pd.read_csv(f'data/{user}_out.csv')

    cols = df.columns
    df.plot.line(x='timestamp', subplots=True, figsize=(24,8))
    plt.title(user)
    plt.savefig(f'data/plot/{user}_out.png')
