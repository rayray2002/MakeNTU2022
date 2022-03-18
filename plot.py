import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', 500)

users = ["A", "B", "C", "D", "E"]
for user in users:
    df = pd.read_csv(f'data/{user}_out.csv')

    cols = df.columns
    df.interpolate(method='linear').plot.line(x='timestamp', subplots=True, figsize=(94,24))
    plt.title(user)
    plt.savefig(f'data/plot/{user}.png')
