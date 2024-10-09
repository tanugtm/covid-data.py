import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the provided JSON file
with open('C:\\Users\\tanug\\Downloads\\covid_states_daily.json')as f:
    covid_data = json.load(f)

# Extract the relevant data from the JSON file
states_daily = covid_data['states_daily']

# Convert the data into a DataFrame for easier analysis
df = pd.DataFrame(states_daily)

# Convert date column to datetime format
df['dateymd'] = pd.to_datetime(df['dateymd'])

# Keep only the confirmed cases where "status" is "Confirmed"
confirmed_cases = df[df['status'] == 'Confirmed']

# Extract the total cases ('tt' column) and the date
confirmed_cases_total = confirmed_cases[['dateymd', 'tt']].copy()

# Convert 'tt' to numeric
confirmed_cases_total['tt'] = pd.to_numeric(confirmed_cases_total['tt'])

# Plotting the total confirmed cases over time
plt.figure(figsize=(10, 6))
plt.plot(confirmed_cases_total['dateymd'], confirmed_cases_total['tt'], color='blue', label='Total Confirmed Cases')
plt.title('Evolution of Total Confirmed COVID-19 Cases Over 515 Days')
plt.xlabel('Date')
plt.ylabel('Total Confirmed Cases')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

# Summary of trends (e.g., rapid increases or decreases)
confirmed_cases_total.describe()