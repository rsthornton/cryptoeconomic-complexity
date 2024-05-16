# Measuring Complexity in Cryptoeconomic Systems
Complexity is often cited as one of the distinguishing qualities of public blockchain networks. However, there have been few, if any, serious efforts aimed at _quantifying_ levels of complexity within these systems. Most existing research has focused on the complexity found in cryptocurrency markets, rather than the systems themselves. 

This project applies information-theoretic measures to explore the complexity of the Bitcoin and Ethereum networks. The goal is to start quantifying this complexity with a holistic focus on their key inputs, outputs, and internal structure, rather than limiting our view to the price dynamics of their tokens.

## Research Question
To what extent can emergence-based information-theoretic complexity measures quantify and clarify the operational dynamics of public blockchain networks?

## Methodology and Data Sources 
### Energy Consumption Data
Energy is a critical input for the operation of public blockchain networks. Daily power demand estimates for Bitcoin and Ethereum were obtained from The University of Cambridge Centre for Alternative Finance's indices, which can be explored further [here](https://ccaf.io/cbnsi/cbeci). 

### Transaction Data
Confirmed transactions represent a key output of public blockchain networks. Daily transaction counts for Bitcoin are sourced from [Blockchain.com](https://www.blockchain.com/explorer/charts/n-transactions), and for Ethereum from [Etherscan](https://etherscan.io/chart/tx). 

### Data Integration 
A [Python script](https://github.com/rsthornton/cryptoeconomic-complexity/blob/main/data/conversion.py) is employed to merge the energy and transaction datasets into a single dataset measuring **"daily transactions per watt."** This metric effectively captures fluctuations in significant inputs and outputs, providing a unified measure to assess the operational dynamics of these networks. 

### Complexity Analysis
An information-theoretic, emergence-based measure of complexity, as detailed in the paper [Emergence in Artificial Life](https://direct.mit.edu/artl/article/29/2/153/114834/Emergence-in-Artificial-Life), is [applied to the integrated data](https://github.com/rsthornton/cryptoeconomic-complexity/blob/main/scripts/complexity_store.py). This methodology allows for the quantification of total complexity on various time scales and the tracking of cumulative complexity over time. 

### Code Implementation 
The analysis is implemented using Python, leveraging libraries such as Pandas for data manipulation and Matplotlib for visualizing the results. The code is structured to facilitate reproducibility and further exploration by peers.

## Initial Results

![btc_weekly_mkt_cap](https://github.com/rsthornton/cryptoeconomic-complexity/assets/5001385/54a3fe5e-21c3-453b-a099-777c7bcb6f14)

![btc_monthly_mkt_cap](https://github.com/rsthornton/cryptoeconomic-complexity/assets/5001385/7aabab97-4241-4013-bcca-7a0ea4620bf2)

![btc_cumulative_mkt_cap](https://github.com/rsthornton/cryptoeconomic-complexity/assets/5001385/bbaf409e-a221-44c1-b305-247a05fe6765)


![eth_weekly_mkt_cap](https://github.com/rsthornton/cryptoeconomic-complexity/assets/5001385/6f105afd-cd77-4aa1-b102-0ecc9791338f)

![eth_monthly_mkt_cap](https://github.com/rsthornton/cryptoeconomic-complexity/assets/5001385/f88b9cd2-6df3-498b-a45d-0a9ed5884409)

![eth_cumulative_mkt_cap](https://github.com/rsthornton/cryptoeconomic-complexity/assets/5001385/00d71b4a-4af4-4ce7-a6a3-568c54dba74d)
