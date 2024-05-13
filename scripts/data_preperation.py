import pandas as pd

def load_and_prepare_data(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Convert the 'Date' column to datetime and set it as the index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Perform any necessary data transformations
    # For example, renaming columns or handling missing values
    # Update this section based on your specific requirements
    
    return df

# Example usage
csv_path = '/Users/shingai/Desktop/cryptoeconomic_complexity/data/master_transactions_per_kw.csv'
data = load_and_prepare_data(csv_path)
print(data.head())

