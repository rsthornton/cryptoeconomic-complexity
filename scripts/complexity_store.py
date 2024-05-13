import pandas as pd
import numpy as np
from data_preperation import data
from state_calculations import data_with_states

def calculate_emergence(probabilities):
    probabilities = probabilities[probabilities > 0]  # Avoid log(0)
    n = len(probabilities)
    if n > 1:
        K = 1 / np.log2(n)
        return -K * np.sum(probabilities * np.log2(probabilities))
    else:
        return 0

def calculate_self_organization(emergence):
    return 1 - emergence

def calculate_complexity(emergence, self_organization):
    return 4 * emergence * self_organization

def calculate_and_store_complexity(df, crypto, time_scale):
    state_column = f"{crypto} Transactions per kW State"
    complexity_column = f"{crypto} {time_scale} Complexity"
    
    def calculate_complexity_for_period(data):
        if not data.empty:
            state_probs = data.value_counts(normalize=True)
            emergence = calculate_emergence(state_probs)
            self_org = calculate_self_organization(emergence)
            complexity = calculate_complexity(emergence, self_org)
            return complexity
        else:
            return np.nan
    
    df[complexity_column] = df[state_column].resample(time_scale).apply(calculate_complexity_for_period)
    
    return df

def calculate_cumulative_complexity(df, crypto):
    state_column = f"{crypto} Transactions per kW State"
    complexity_column = f"{crypto} Cumulative Complexity"
    
    cumulative_complexity = []
    for i in range(len(df)):
        data_slice = df.iloc[:i+1][state_column]
        state_probs = data_slice.value_counts(normalize=True)
        emergence = calculate_emergence(state_probs)
        self_org = calculate_self_organization(emergence)
        complexity = calculate_complexity(emergence, self_org)
        cumulative_complexity.append(complexity)
    
    df[complexity_column] = cumulative_complexity
    
    return df

def calculate_and_store_complexity_measures(df, cryptos, time_scales):
    for crypto in cryptos:
        for time_scale in time_scales:
            df = calculate_and_store_complexity(df, crypto, time_scale)
        
        df = calculate_cumulative_complexity(df, crypto)
    
    return df

# Constants
CRYPTOS = ['Bitcoin', 'Ethereum']
TIME_SCALES = ['W', 'M']  # W for weekly, M for monthly

# Calculate and store complexity measures
data_with_complexity = calculate_and_store_complexity_measures(data_with_states, CRYPTOS, TIME_SCALES)

print(data_with_complexity.head())