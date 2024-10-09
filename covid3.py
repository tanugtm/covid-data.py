import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load the provided JSON file
with open('C:\\Users\\tanug\\Downloads\\covid_states_daily.json') as f:
    covid_data = json.load(f)

# Extract the relevant data
states_daily = covid_data['states_daily']

# Convert the data into a DataFrame
df = pd.DataFrame(states_daily)

# Convert date column to datetime format
df['dateymd'] = pd.to_datetime(df['dateymd'])

# Filter the data for the state and keep only the relevant status ('Confirmed', 'Recovered')
state_code = "mh"  # Maharashtra (you can change this to other state codes like 'dl' for Delhi, etc.)
confirmed_cases = df[(df['status'] == 'Confirmed')][['dateymd', state_code]].copy()
recovered_cases = df[(df['status'] == 'Recovered')][['dateymd', state_code]].copy()

# Rename columns for clarity
confirmed_cases.columns = ['date', 'confirmed']
recovered_cases.columns = ['date', 'recovered']

# Merge the data on date
merged_data = pd.merge(confirmed_cases, recovered_cases, on='date', how='left')

# Convert confirmed and recovered to numeric, forcing errors to NaN
merged_data['confirmed'] = pd.to_numeric(merged_data['confirmed'], errors='coerce')
merged_data['recovered'] = pd.to_numeric(merged_data['recovered'], errors='coerce')

# Drop rows with missing values (if any)
merged_data.dropna(inplace=True)

# Prepare data for linear regression
X = merged_data['confirmed'].values.reshape(-1, 1)  # confirmed cases as input
y = merged_data['recovered'].values  # recovered cases as output

# Create a linear regression model
model = LinearRegression()
model.fit(X, y)

# Get the predictions and the equation of the line
y_pred = model.predict(X)
intercept = model.intercept_
slope = model.coef_[0]

# Compute the correlation coefficient (R^2)
r_squared = r2_score(y, y_pred)

# Plot the scatter plot and the regression line
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Actual Recovered Cases')
plt.plot(X, y_pred, color='red', label=f'Fitted Line: y = {slope:.2f}x + {intercept:.2f}')
plt.title(f'Relationship Between Confirmed and Recovered Cases for {state_code.upper()}')
plt.xlabel('Confirmed Cases')
plt.ylabel('Recovered Cases')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Print the linear equation and R^2 value
print(f"Linear Equation: y = {slope:.2f}x + {intercept:.2f}")
print(f"R^2 (Correlation Coefficient): {r_squared:.4f}")
