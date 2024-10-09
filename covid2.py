import json
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load the provided JSON file
with open('C:\\Users\\tanug\\Downloads\\covid_states_daily.json') as f:
    covid_data = json.load(f)

# Extract the relevant data
states_daily = covid_data['states_daily']

# Convert the data into a DataFrame
df = pd.DataFrame(states_daily)

# Convert date column to datetime format
df['dateymd'] = pd.to_datetime(df['dateymd'])

# Filter the data for the state and keep only the relevant status ('Confirmed', 'Recovered', 'Deceased')
state_code = "mh"  # Maharashtra (you can change this to other state codes like 'dl' for Delhi, etc.)
confirmed_cases = df[(df['status'] == 'Confirmed')][['dateymd', state_code]].copy()
recovered_cases = df[(df['status'] == 'Recovered')][['dateymd', state_code]].copy()
deceased_cases = df[(df['status'] == 'Deceased')][['dateymd', state_code]].copy()

# Rename columns for clarity
confirmed_cases.columns = ['date', 'confirmed']
recovered_cases.columns = ['date', 'recovered']
deceased_cases.columns = ['date', 'deceased']

# Merge the data on date
merged_data = pd.merge(confirmed_cases, recovered_cases, on='date', how='left')
merged_data = pd.merge(merged_data, deceased_cases, on='date', how='left')

# Convert confirmed, recovered, and deceased to numeric, forcing errors to NaN
merged_data['confirmed'] = pd.to_numeric(merged_data['confirmed'], errors='coerce')
merged_data['recovered'] = pd.to_numeric(merged_data['recovered'], errors='coerce')
merged_data['deceased'] = pd.to_numeric(merged_data['deceased'], errors='coerce')

# Fill missing values with 0 (if any)
merged_data.fillna(0, inplace=True)

# Calculate active cases
merged_data['active'] = merged_data['confirmed'] - (merged_data['recovered'] + merged_data['deceased'])

# Set the date as the index
merged_data.set_index('date', inplace=True)

# ARIMA model to predict next 10 days of active cases
active_cases = merged_data['active']

# Fit ARIMA model (p, d, q) can be adjusted based on data trends
model = ARIMA(active_cases, order=(5, 1, 2))
model_fit = model.fit()

# Forecast for the next 10 days
forecast = model_fit.forecast(steps=10)

# Plot the active cases and the forecast
plt.figure(figsize=(10, 6))
plt.plot(active_cases.index, active_cases, label='Historical Active Cases', color='blue')
plt.plot(pd.date_range(start=active_cases.index[-1], periods=11, freq='D')[1:], forecast, label='Forecasted Active Cases', color='red')
plt.title(f'COVID-19 Active Cases Prediction for {state_code.upper()}')
plt.xlabel('Date')
plt.ylabel('Active Cases')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

# Print the forecasted values
print(forecast)

