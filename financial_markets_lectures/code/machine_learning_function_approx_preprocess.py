import pandas as pd

from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("function_approx.csv")
print(f"Data before scaling {df['y'].min()}, {df['y'].max()}")

scale_X = MinMaxScaler()
scale_y = MinMaxScaler()

X_scaled = scale_X.fit_transform(df[['X']])
y_scaled = scale_y.fit_transform(df[['y']])

print(f"The same data after scaling {y_scaled.min()}, {y_scaled.max()}")

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_scaled, test_size=0.2)
