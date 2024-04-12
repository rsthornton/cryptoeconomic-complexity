import pandas as pd

# Load the data
btc_transactions = pd.read_csv('btc_transactions.csv')
btc_energy = pd.read_csv('btc_energy.csv', skiprows=1)
eth_transactions = pd.read_csv('eth_transactions.csv')
eth1_energy = pd.read_csv('eth1_energy.csv', skiprows=1)
eth2_energy = pd.read_csv('eth2_energy.csv', skiprows=0)

# Convert 'Date' column to datetime
btc_transactions['Date'] = pd.to_datetime(btc_transactions['Date'])
btc_energy['Date'] = pd.to_datetime(btc_energy['Date and Time'])
btc_energy.drop(['Timestamp', 'Date and Time'], axis=1, inplace=True)
eth_transactions['Date'] = pd.to_datetime(eth_transactions['Date(UTC)'], format='%m/%d/%Y')
eth1_energy['Date'] = pd.to_datetime(eth1_energy['Date and Time'])
eth1_energy.drop('Date and Time', axis=1, inplace=True)
eth2_energy['Date'] = pd.to_datetime(eth2_energy['Date and Time'])
eth2_energy.drop('Date and Time', axis=1, inplace=True)

# Ensure all data is in the expected format
btc_transactions['Transactions'] = btc_transactions['Transactions'].astype(float)
eth_transactions['Value'] = eth_transactions['Value'].astype(float)

# Convert Bitcoin's energy consumption from GW to kW
btc_energy['Energy Consumption (kW)'] = btc_energy['power GUESS, GW'] * 1e6

# Convert energy consumption from GW to kW for eth1_energy
eth1_energy['Energy Consumption (kW)'] = eth1_energy['power GUESS, GW'] * 1e6

# Delete entries after 2022-09-14 from eth1_energy
eth1_energy = eth1_energy[eth1_energy['Date'] <= '2022-09-14']

# Filter eth2_energy to only include data from 2022-09-15 onwards
eth2_energy = eth2_energy[eth2_energy['Date'] >= '2022-09-15']

#Quest
eth2_energy['Energy Consumption (kW)'] = eth2_energy['power GUESS, kW']


# Combine eth1_energy and eth2_energy
eth_energy = pd.concat([eth1_energy, eth2_energy])

# Merge the datasets on the date column
btc_data = pd.merge(btc_transactions, btc_energy, on='Date', how='outer')
eth_data = pd.merge(eth_transactions, eth_energy, on='Date', how='outer')

# Calculate transactions per kW for both cryptocurrencies
btc_data['Transactions per kW'] = btc_data['Transactions'] / btc_data['Energy Consumption (kW)']
eth_data['Transactions per kW'] = eth_data['Value'] / eth_data['Energy Consumption (kW)']

# Merge Bitcoin and Ethereum data into a master DataFrame
master_data = btc_data[['Date', 'Transactions per kW']].copy()
master_data.rename(columns={'Transactions per kW': 'Bitcoin Transactions per kW'}, inplace=True)
master_data = pd.merge(master_data, eth_data[['Date', 'Transactions per kW']], on='Date', how='outer')

# Rename the 'Transactions per kW' column for Ethereum
master_data.rename(columns={'Transactions per kW': 'Ethereum Transactions per kW'}, inplace=True)


# Filter out dates from 2010-07-18 through 2011-09-01 and all dates after 2024-03-29
master_data = master_data[((master_data['Date'] < '2010-07-18') | (master_data['Date'] > '2011-09-02')) & (master_data['Date'] <= '2024-03-29')]

# Save the filtered master data to a new CSV file
master_data.to_csv('master_transactions_per_kw.csv', index=False)