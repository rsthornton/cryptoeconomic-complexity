import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants for the script
MASTER_CSV_PATH = '/Users/shingai/Desktop/cryptoeconomic_complexity/data/master_transactions_per_kw.csv'
CRYPTOS = ['Bitcoin', 'Ethereum']
TIME_SCALES = ['D', 'W', 'M', 'Y']  # D for daily, W for weekly, M for monthly, Y for yearly
STATE_PERCENTILES = [10, 30, 70, 90]
STATE_LABELS = ['Very Low', 'Low', 'High', 'Very High', 'Extremely High']

# Load and prepare data
def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

# Define states based on value and percentiles
def define_states(value, percentiles, labels):
    for i, percentile in enumerate(percentiles):
        if value < percentile:
            return labels[i]
    return labels[-1]

# Calculate percentiles and apply state definition for each cryptocurrency
def apply_state_definitions(df, cryptos, percentiles, labels):
    for crypto in cryptos:
        crypto_column = f"{crypto} Transactions per kW"
        state_column = f"{crypto} Transactions per kW State"
        crypto_df = df[crypto_column].dropna()
        percentile_values = np.percentile(crypto_df, percentiles)
        df[state_column] = crypto_df.apply(lambda x: define_states(x, percentile_values, labels))
    return df

# Calculate emergence measure
def calculate_emergence(probabilities):
    probabilities = probabilities[probabilities > 0]  # Avoid log(0)
    n = len(probabilities)
    if n > 1:
        K = 1 / np.log2(n)
        return -K * np.sum(probabilities * np.log2(probabilities))
    else:
        return 0

# Calculate self-organization measure
def calculate_self_organization(emergence):
    return 1 - emergence

# Calculate complexity measure
def calculate_complexity(emergence, self_organization):
    return 4 * emergence * self_organization

# Calculate complexity measures for a cryptocurrency at different time scales
def calculate_complexity_measures(df, crypto, time_scales):
    state_column = f"{crypto} Transactions per kW State"
    complexities = {}

    for scale in time_scales:
        print(f"\nCalculating complexity for {crypto} Transactions per Watt at {scale} scale:")
        resampled_series = df[state_column].resample(scale).apply(lambda x: x.value_counts().index[0] if not x.isnull().all() else np.nan)
        state_probs = resampled_series.value_counts(normalize=True)
        emergence = calculate_emergence(state_probs)
        print(f"Emergence ({scale} scale): {emergence:.6f}")
        self_org = calculate_self_organization(emergence)
        print(f"Self-organization ({scale} scale): {self_org:.6f}")
        complexity = calculate_complexity(emergence, self_org)
        complexities[scale] = complexity
        print(f"Complexity ({scale} scale): {complexity:.6f}")

    return complexities

# Plot complexity measures
def plot_complexity_measures(complexities, crypto, color):
    plt.figure(figsize=(8, 6))
    plt.bar(complexities.keys(), complexities.values(), color=color)
    plt.xlabel('Time Scale')
    plt.ylabel('Complexity')
    plt.title(f'Complexity Measures for {crypto} Transactions per Watt at Different Time Scales')
    plt.tight_layout()
    plt.show()


# Calculate cumulative complexity up to each day
def calculate_cumulative_complexity(df, crypto):
    state_column = f"{crypto} Transactions per kW State"
    cumulative_complexity = []
    
    for i in range(len(df)):
        data_slice = df.iloc[:i+1][state_column]
        state_probs = data_slice.value_counts(normalize=True)
        emergence = calculate_emergence(state_probs)
        self_org = calculate_self_organization(emergence)
        complexity = calculate_complexity(emergence, self_org)
        cumulative_complexity.append(complexity)
    
    return pd.Series(cumulative_complexity, index=df.index)

# Plot cumulative complexity over time
def plot_cumulative_complexity(df, crypto, color):
    cumulative_complexity = calculate_cumulative_complexity(df, crypto)
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_complexity, color=color, label=crypto)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Complexity')
    plt.title(f'Cumulative Complexity for {crypto} Transactions per Watt')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main function to orchestrate the analysis
def main():
    df = load_and_prepare_data(MASTER_CSV_PATH)
    df = apply_state_definitions(df, CRYPTOS, STATE_PERCENTILES, STATE_LABELS)
    
    for crypto, color in zip(CRYPTOS, ['orange', 'blue']):
        complexities = calculate_complexity_measures(df, crypto, TIME_SCALES)
        plot_complexity_measures(complexities, crypto, color)
        plot_cumulative_complexity(df, crypto, color)

if __name__ == "__main__":
    main()