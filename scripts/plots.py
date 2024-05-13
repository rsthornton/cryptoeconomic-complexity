import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_preperation import data
from state_calculations import data_with_states
from complexity import calculate_emergence, calculate_self_organization, calculate_complexity, CRYPTOS, complexity_results

def plot_complexity_measures(complexities, crypto, color):
    plt.figure(figsize=(8, 6))
    plt.bar(complexities.keys(), complexities.values(), color=color)
    plt.xlabel('Time Scale')
    plt.ylabel('Complexity')
    plt.title(f'Complexity Measures for {crypto} Transactions per Watt at Different Time Scales')
    plt.tight_layout()
    plt.show()

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

def plot_weekly_complexity(df, crypto, color):
    weekly_complexity = calculate_weekly_complexity(df, crypto)
    if not weekly_complexity.empty:
        smoothed_complexity = apply_ema(weekly_complexity['Complexity'], span=12)
        
        plt.figure(figsize=(12, 6))
        plt.plot(weekly_complexity.index, smoothed_complexity, color=color, label=crypto)
        plt.xlabel('Date')
        plt.ylabel('Weekly Complexity (Smoothed)')
        plt.title(f'Weekly Complexity for {crypto} Transactions per Watt (Smoothed)')
        plt.legend()
        plt.tight_layout()
        plt.show()

def calculate_weekly_complexity(df, crypto):
    state_column = f"{crypto} Transactions per kW State"
    weekly_complexity = []
    
    start_date = df.index.min()
    end_date = df.index.max()
    weeks = pd.date_range(start=start_date, end=end_date, freq='W')
    
    for week_start, week_end in zip(weeks[:-1], weeks[1:]):
        if week_start in df.index and week_end in df.index:
            data_slice = df.loc[week_start:week_end][state_column]
            if not data_slice.empty:
                state_probs = data_slice.value_counts(normalize=True)
                emergence = calculate_emergence(state_probs)
                self_org = calculate_self_organization(emergence)
                complexity = calculate_complexity(emergence, self_org)
            else:
                complexity = np.nan
            weekly_complexity.append({'Date': week_end, 'Complexity': complexity})
    
    if weekly_complexity:
        weekly_complexity_df = pd.DataFrame(weekly_complexity, columns=['Date', 'Complexity']).set_index('Date')
        return weekly_complexity_df
    else:
        return pd.DataFrame()

def apply_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

def plot_monthly_complexity(df, crypto, color):
    monthly_complexity = calculate_monthly_complexity(df, crypto)
    if not monthly_complexity.empty:
        smoothed_complexity = apply_ema(monthly_complexity['Complexity'], span=12)
        
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_complexity.index, smoothed_complexity, color=color, label=crypto)
        plt.xlabel('Date')
        plt.ylabel('Monthly Complexity (Smoothed)')
        plt.title(f'Monthly Complexity for {crypto} Transactions per Watt (Smoothed)')
        plt.legend()
        plt.tight_layout()
        plt.show()

def calculate_monthly_complexity(df, crypto):
    state_column = f"{crypto} Transactions per kW State"
    monthly_complexity = []
    
    for month_start, month_end in zip(df.resample('MS').first().index, df.resample('M').last().index):
        if month_start in df.index and month_end in df.index:
            data_slice = df.loc[month_start:month_end][state_column]
            state_probs = data_slice.value_counts(normalize=True)
            emergence = calculate_emergence(state_probs)
            self_org = calculate_self_organization(emergence)
            complexity = calculate_complexity(emergence, self_org)
            monthly_complexity.append({'Date': month_end, 'Complexity': complexity})
    
    if monthly_complexity:
        monthly_complexity_df = pd.DataFrame(monthly_complexity, columns=['Date', 'Complexity']).set_index('Date')
        return monthly_complexity_df
    else:
        return pd.DataFrame()

def plot_weekly_complexity_marketcap(df, crypto, color):
    marketcap_col = f"{crypto.lower()}_market_cap"
    weekly_complexity_marketcap = calculate_weekly_complexity_marketcap(df, crypto, marketcap_col)
    
    if not weekly_complexity_marketcap.empty:
        smoothed_complexity = apply_ema(weekly_complexity_marketcap['Complexity'], span=12)  # Apply smoothing to complexity
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        
        ax1.plot(weekly_complexity_marketcap.index, smoothed_complexity, color=color, label=f"{crypto} Complexity (Smoothed)")  # Use smoothed complexity
        ax2.plot(weekly_complexity_marketcap.index, weekly_complexity_marketcap['Market Cap'], color='green', label=f"{crypto} Market Cap")
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Weekly Complexity (Smoothed)')  # Update y-label
        ax2.set_ylabel('Market Cap')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.title(f"Weekly Complexity (Smoothed) and Market Cap for {crypto}")  # Update title
        plt.tight_layout()
        plt.show()

def calculate_weekly_complexity_marketcap(df, crypto, marketcap_col):
    state_column = f"{crypto} Transactions per kW State"
    weekly_complexity_marketcap = []
    
    start_date = df.index.min()
    end_date = df.index.max()
    weeks = pd.date_range(start=start_date, end=end_date, freq='W')
    
    for week_start, week_end in zip(weeks[:-1], weeks[1:]):
        if week_start in df.index and week_end in df.index:
            data_slice = df.loc[week_start:week_end][[state_column, marketcap_col]]
            if not data_slice.empty:
                state_probs = data_slice[state_column].value_counts(normalize=True)
                emergence = calculate_emergence(state_probs)
                self_org = calculate_self_organization(emergence)
                complexity = calculate_complexity(emergence, self_org)
                market_cap = data_slice[marketcap_col].mean()
                weekly_complexity_marketcap.append({'Date': week_end, 'Complexity': complexity, 'Market Cap': market_cap})
    
    if weekly_complexity_marketcap:
        weekly_complexity_marketcap_df = pd.DataFrame(weekly_complexity_marketcap, columns=['Date', 'Complexity', 'Market Cap']).set_index('Date')
        return weekly_complexity_marketcap_df
    else:
        return pd.DataFrame()

def plot_monthly_complexity_marketcap(df, crypto, color):
    marketcap_col = f"{crypto.lower()}_market_cap"
    monthly_complexity_marketcap = calculate_monthly_complexity_marketcap(df, crypto, marketcap_col)
    
    if not monthly_complexity_marketcap.empty:
        smoothed_complexity = apply_ema(monthly_complexity_marketcap['Complexity'], span=12)  # Apply smoothing to complexity
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        
        ax1.plot(monthly_complexity_marketcap.index, smoothed_complexity, color=color, label=f"{crypto} Complexity (Smoothed)")  # Use smoothed complexity
        ax2.plot(monthly_complexity_marketcap.index, monthly_complexity_marketcap['Market Cap'], color='green', label=f"{crypto} Market Cap")
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Monthly Complexity (Smoothed)')  # Update y-label
        ax2.set_ylabel('Market Cap')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.title(f"Monthly Complexity (Smoothed) and Market Cap for {crypto}")  # Update title
        plt.tight_layout()
        plt.show()

def calculate_monthly_complexity_marketcap(df, crypto, marketcap_col):
    state_column = f"{crypto} Transactions per kW State"
    monthly_complexity_marketcap = []
    
    for month_start, month_end in zip(df.resample('MS').first().index, df.resample('M').last().index):
        if month_start in df.index and month_end in df.index:
            data_slice = df.loc[month_start:month_end][[state_column, marketcap_col]]
            state_probs = data_slice[state_column].value_counts(normalize=True)
            emergence = calculate_emergence(state_probs)
            self_org = calculate_self_organization(emergence)
            complexity = calculate_complexity(emergence, self_org)
            market_cap = data_slice[marketcap_col].mean()
            monthly_complexity_marketcap.append({'Date': month_end, 'Complexity': complexity, 'Market Cap': market_cap})
    
    if monthly_complexity_marketcap:
        monthly_complexity_marketcap_df = pd.DataFrame(monthly_complexity_marketcap, columns=['Date', 'Complexity', 'Market Cap']).set_index('Date')
        return monthly_complexity_marketcap_df
    else:
        return pd.DataFrame()

def plot_cumulative_complexity_marketcap(df, crypto, color):
    marketcap_col = f"{crypto.lower()}_market_cap"
    cumulative_complexity_marketcap = calculate_cumulative_complexity_marketcap(df, crypto, marketcap_col)
    
    if not cumulative_complexity_marketcap.empty:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = ax1.twinx()
        
        ax1.plot(cumulative_complexity_marketcap.index, cumulative_complexity_marketcap['Complexity'], color=color, label=f"{crypto} Complexity")
        ax2.plot(cumulative_complexity_marketcap.index, cumulative_complexity_marketcap['Market Cap'], color='green', label=f"{crypto} Market Cap")
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Cumulative Complexity')
        ax2.set_ylabel('Market Cap')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.title(f"Cumulative Complexity and Market Cap for {crypto}")
        plt.tight_layout()
        plt.show()

def calculate_cumulative_complexity_marketcap(df, crypto, marketcap_col):
    state_column = f"{crypto} Transactions per kW State"
    cumulative_complexity_marketcap = []
    
    for i in range(len(df)):
        data_slice = df.iloc[:i+1][[state_column, marketcap_col]]
        state_probs = data_slice[state_column].value_counts(normalize=True)
        emergence = calculate_emergence(state_probs)
        self_org = calculate_self_organization(emergence)
        complexity = calculate_complexity(emergence, self_org)
        market_cap = data_slice[marketcap_col].iloc[-1]  # Use the last market cap value instead of the mean
        cumulative_complexity_marketcap.append({'Date': df.index[i], 'Complexity': complexity, 'Market Cap': market_cap})
    
    if cumulative_complexity_marketcap:
        cumulative_complexity_marketcap_df = pd.DataFrame(cumulative_complexity_marketcap, columns=['Date', 'Complexity', 'Market Cap']).set_index('Date')
        return cumulative_complexity_marketcap_df
    else:
        return pd.DataFrame()

# Plotting
for crypto, color in zip(CRYPTOS, ['orange', 'blue']):
    plot_complexity_measures(complexity_results[crypto], crypto, color)
    plot_cumulative_complexity(data_with_states, crypto, color)
    plot_weekly_complexity(data_with_states, crypto, color)
    plot_monthly_complexity(data_with_states, crypto, color)
    plot_weekly_complexity_marketcap(data, crypto, color)
    plot_monthly_complexity_marketcap(data, crypto, color)
    plot_cumulative_complexity_marketcap(data, crypto, color)