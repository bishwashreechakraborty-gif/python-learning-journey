import pandas as pd
import os
from sklearn.linear_model import LinearRegression

# File path fix
file_path = os.path.join(os.path.dirname(__file__), "data.csv")
df = pd.read_csv(file_path)

X = df[["area"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

area = int(input("Enter area: "))

# FIX HERE
input_data = pd.DataFrame([[area]], columns=["area"])
predicted_price = model.predict(input_data)

print("Predicted Price:", predicted_price[0])