import pandas as pd

df = pd.read_excel("https://github.com/matteosan1/finance_course/raw/master/input_files/stock_market.xlsx")
print (len(df))
print (df.head())

print(df[df.duplicated() == True])

print ("Before duplicates removal: {}".format(len(df)))
df.drop_duplicates(inplace=True)
print ("After duplicates removal: {}".format(len(df)))

print (df[df.isna().any(axis=1)])

print ("Before NaN removal: {}".format(len(df)))
df.dropna(inplace=True)
print ("After NaN removal: {}".format(len(df)))


pos_var = df.loc[df["Delta"] > 0, :]
print (len(pos_var))
print (pos_var.head())

highest_price = df.sort_values(by=['Price'], ascending = True)
print (highest_price[:5])


import pandas as pf
from datetime import date
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("https://raw.githubusercontent.com/matteosan1/finance_course/develop/input_files/exercise_5.28.csv")
print (df.head())
dfs = df['dfs']
pillars = [d.date() for d in pd.to_datetime(df['pillars'])]

plt.plot(pillars, dfs, marker="o", label="EUR6M d.f.")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# this one instead rotate labels to avoid superimposition
plt.xticks(rotation=45)
plt.xlabel("Pillar dates")
plt.ylabel("Discount Factors")
plt.grid(True)
plt.legend()
plt.show()
