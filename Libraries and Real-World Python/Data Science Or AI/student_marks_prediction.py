import pandas as pd
import os
from sklearn.linear_model import LinearRegression

# Fix file path
file_path = os.path.join(os.path.dirname(__file__), "data.csv")
df = pd.read_csv(file_path)

X = df[["hours"]]
y = df["marks"]

model = LinearRegression()
model.fit(X, y)

hours = float(input("Enter study hours: "))

# Fix warning also (best practice)
input_data = pd.DataFrame([[hours]], columns=["hours"])
predicted_marks = model.predict(input_data)

print("Predicted Marks:", predicted_marks[0])