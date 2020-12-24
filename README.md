# ripple_network_analysis

Requirements

* pyvis (https://pyvis.readthedocs.io/en/latest/) (Network visualization package)
* NetworkX (https://networkx.org/) (Network analysis package)
* requests (API request package)
* matplotlib (Python plotting library)

## Fetching Data

#### API Method:
Since our study focuses on trust set network in the Ripple, we used the method specifically to get the transactions related to creating, updating or removing trust lines between the wallets. The method used in fetching data is {/v2/transactions/} and it accepts parameter such as {start} in form of timestamp string, which filter results to this time and later, {end} which filter results to this time and earlier, {type} which accepts string and filters the transactions to specific type (In our case it is {TrustSet}).

**To download the data from API :**

Run the **"Data_downloading_and_parsing_0.6.py"** python file with **Start date** and **End date** as arguments.
```
cd CODE

python Data_downloading_and_parsing_0.6.py 2019-01-01 2019-01-07
```
Running this code will give Parsed Data file for trustset transactions in .CSV format stored in Data directory. **Logs** would be written in the CODE directory.

## Network Analysis

Trust lines network visualization was generated using **pyvis** module and for the analysis of the network **NetworkX** python package was used. 
This section presents the analysis on the network generated from the trust set transactions data. We observe the top trusted wallets and currencies used in the trust transactions between the wallets. We also study the pattern of trust between two wallets. We observe pattern of transactions involved with top nodes.

code filename: "Analysis_code.py"

Apart from calulating network metrics using inbuilt functions of **NetworkX** we created some user functions.
```
various user functions used:
transactions_graph : This function generates a transactions graph
check_change_in_trustset : This function outputs an average time in minutes at which trust is changing between 2 accounts mentioned
filter_transactions: This function filters the transaction data for latest transaction between accounts to get the current state of network for creating a graph
generate_trustline_graph: This function generates a network graph using pyvis module. The graph is saved in Analysis folder
```
