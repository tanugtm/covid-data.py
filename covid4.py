import json
import pandas as pd
import numpy as np
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

# Filter the data for confirmed and recovered cases
confirmed_cases = df[df['status'] == 'Confirmed'].copy()
recovered_cases = df[df['status'] == 'Recovered'].copy()

# State name mapping: map state abbreviations to full names
state_mapping = {
    "an": "Andaman and Nicobar Islands", "ap": "Andhra Pradesh", "ar": "Arunachal Pradesh", "as": "Assam",
    "br": "Bihar", "ch": "Chandigarh", "ct": "Chhattisgarh", "dl": "Delhi", "dn": "Dadra and Nagar Haveli and Daman and Diu",
    "ga": "Goa", "gj": "Gujarat", "hp": "Himachal Pradesh", "hr": "Haryana", "jh": "Jharkhand", "jk": "Jammu and Kashmir",
    "ka": "Karnataka", "kl": "Kerala", "la": "Ladakh", "ld": "Lakshadweep", "mh": "Maharashtra", "ml": "Meghalaya",
    "mn": "Manipur", "mp": "Madhya Pradesh", "mz": "Mizoram", "nl": "Nagaland", "or": "Odisha", "pb": "Punjab",
    "py": "Puducherry", "rj": "Rajasthan", "sk": "Sikkim", "tg": "Telangana", "tn": "Tamil Nadu", "tr": "Tripura",
    "up": "Uttar Pradesh", "ut": "Uttarakhand", "wb": "West Bengal", "tt": "India Total"
}

# List of state codes (excluding 'tt' for total India)
state_codes = [code for code in state_mapping if code != "tt"]

# Initialize a dictionary to store recovery rates for each state
recovery_rates = {}

# Calculate the recovery rate for each state
for state in state_codes:
    # Get total confirmed and recovered cases for each state
    total_confirmed = pd.to_numeric(confirmed_cases[state], errors='coerce').sum()
    total_recovered = pd.to_numeric(recovered_cases[state], errors='coerce').sum()

    # Avoid division by zero by checking if total_confirmed is greater than zero
    if total_confirmed > 0:
        recovery_rate = (total_recovered / total_confirmed) * 100
    else:
        recovery_rate = 0  # Set to 0 if no confirmed cases

    # Use full state name in the dictionary
    recovery_rates[state_mapping[state]] = recovery_rate

# Convert the recovery rates dictionary into a DataFrame for easier manipulation
recovery_rates_df = pd.DataFrame(list(recovery_rates.items()), columns=['State', 'Recovery Rate'])

# Sort states by recovery rate (highest to lowest)
recovery_rates_df.sort_values(by='Recovery Rate', ascending=False, inplace=True)

# Plotting the recovery rates as a bar chart
plt.figure(figsize=(12, 8))
plt.barh(recovery_rates_df['State'], recovery_rates_df['Recovery Rate'], color='skyblue')
plt.xlabel('Recovery Rate (%)')
plt.ylabel('States')
plt.title('COVID-19 Recovery Rates Across States Over 515 Days')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()

# Print the top 5 and bottom 5 states by recovery rate
top_5_states = recovery_rates_df.head()
bottom_5_states = recovery_rates_df.tail()
print("Top 5 States by Recovery Rate:")
print(top_5_states)
print("\nBottom 5 States by Recovery Rate:")
print(bottom_5_states)
