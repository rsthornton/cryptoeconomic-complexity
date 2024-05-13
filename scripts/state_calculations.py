import pandas as pd
import numpy as np
from data_preperation import data

def define_states(value, percentiles, labels):
    for i, percentile in enumerate(percentiles):
        if value < percentile:
            return labels[i]
    return labels[-1]

def apply_state_definitions(df, cryptos, percentiles, labels):
    for crypto in cryptos:
        crypto_column = f"{crypto} Transactions per kW"
        state_column = f"{crypto} Transactions per kW State"
        crypto_df = df[crypto_column].dropna()
        percentile_values = np.percentile(crypto_df, percentiles)
        df[state_column] = crypto_df.apply(lambda x: define_states(x, percentile_values, labels))
    return df

# Example usage
CRYPTOS = ['Bitcoin', 'Ethereum']
STATE_PERCENTILES = [10, 30, 70, 90]
STATE_LABELS = ['Very Low', 'Low', 'High', 'Very High', 'Extremely High']

# Assuming you have loaded the data into a DataFrame called 'data'
data_with_states = apply_state_definitions(data, CRYPTOS, STATE_PERCENTILES, STATE_LABELS)
print(data_with_states.head())