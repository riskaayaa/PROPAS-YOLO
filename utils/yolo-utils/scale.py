import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# Load the data
data = {
    "Data": ["bandung", "polman3", "papua", "kalteng", "balikpapan", "riau", "garut", "polman", "polman2", "semarang"],
    "dim": [3623, 2254, 5100, 2698, 5064, 4098, 2225, 2060, 1483, 4100],
    "gsd": [0.150, 0.250, 0.150, 0.150, 0.045, 0.150, 0.100, 0.250, 0.250, 0.100],
    "luas": [29.53, 31.75, 58.52, 16.38, 5.19, 37.79, 4.95, 26.52, 13.75, 16.81],
    "dim_plus": [3840, 2560, 5120, 2880, 5120, 4160, 2240, 2240, 1600, 4160],
    "scale": [1.059, 1.135, 1.054, 1.043, 1.011, 1.065, 1.034, 1.117, 1.033, 1.061]
}

df = pd.DataFrame(data)

# Separate features and target
X = df[['dim', 'gsd', 'luas', 'dim_plus']]
y = df['scale']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Perform polynomial regression
poly_features = PolynomialFeatures(degree=2)
X_train_poly = poly_features.fit_transform(X_train)
X_test_poly = poly_features.transform(X_test)

model = LinearRegression()
model.fit(X_train_poly, y_train)

# Predict the 'scale' values
y_pred = model.predict(X_test_poly)

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)

print("Mean Squared Error:", mse)
print(y_pred)
