import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import mutual_info_score
from complexity_store import data_with_complexity
import dataframe_image as dfi

def calculate_correlations(data, crypto, complexity_col, marketcap_col, n_bins=10):
    # Extract the relevant columns from the data
    complexity = data[complexity_col]
    market_cap = data[marketcap_col]

    # Remove rows with missing or invalid values
    valid_data = pd.concat([complexity, market_cap], axis=1).dropna()
    complexity = valid_data[complexity_col]
    market_cap = valid_data[marketcap_col]

    # Calculate Pearson correlation coefficient and p-value
    pearson_corr, pearson_p = stats.pearsonr(complexity, market_cap)

    # Calculate Spearman correlation coefficient and p-value
    spearman_corr, spearman_p = stats.spearmanr(complexity, market_cap)

    # Discretize complexity and market cap values into bins
    complexity_bins = pd.cut(complexity, bins=n_bins, labels=False)
    market_cap_bins = pd.cut(market_cap, bins=n_bins, labels=False)

    # Calculate mutual information using the discretized values
    mutual_info = mutual_info_score(complexity_bins, market_cap_bins)

    # Create a DataFrame to store the correlation measures
    corr_data = {
        'Blockchain': [crypto],
        'Pearson Correlation': [pearson_corr],
        'Pearson p-value': [pearson_p],
        'Spearman Correlation': [spearman_corr],
        'Spearman p-value': [spearman_p],
        'Mutual Information': [mutual_info]
    }
    corr_df = pd.DataFrame(corr_data)

    return corr_df

def analyze_correlations(data, cryptos, complexity_type):
    all_corr_df = pd.DataFrame()
    for crypto in cryptos:
        if complexity_type == 'weekly':
            complexity_col = f"{crypto} W Complexity"
        elif complexity_type == 'monthly':
            complexity_col = f"{crypto} M Complexity"
        elif complexity_type == 'cumulative':
            complexity_col = f"{crypto} Cumulative Complexity"
        else:
            raise ValueError("Invalid complexity type. Choose from 'weekly', 'monthly', or 'cumulative'.")
        marketcap_col = f"{crypto.lower()}_market_cap"

        # Calculate correlations for the current cryptocurrency
        corr_df = calculate_correlations(data, crypto, complexity_col, marketcap_col)

        # Append the results to the overall DataFrame
        all_corr_df = pd.concat([all_corr_df, corr_df], ignore_index=True)

    return all_corr_df

# Constants
CRYPTOS = ['Bitcoin', 'Ethereum']
COMPLEXITY_TYPE = 'monthly' # Choose from 'weekly', 'monthly', or 'cumulative'

# Calculate correlation results
correlation_results = analyze_correlations(data_with_complexity, CRYPTOS, COMPLEXITY_TYPE)

# Format p-values to display in scientific notation
correlation_results['Pearson p-value'] = correlation_results['Pearson p-value'].apply(lambda x: '{:.2e}'.format(x))
correlation_results['Spearman p-value'] = correlation_results['Spearman p-value'].apply(lambda x: '{:.2e}'.format(x))

styled_table = correlation_results.style.set_properties(**{'text-align': 'center'}).set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
dfi.export(styled_table, 'correlation_table.png', table_conversion='matplotlib')