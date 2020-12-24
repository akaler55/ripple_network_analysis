# -*- coding: utf-8 -*-
"""
@author: Amandeep Singh, Rahul
"""

'''
This Program presents the functions and code used for analysis of the Trustset 
transactions fetched using the other code.
'''

# INSTALLING IMPORTANT LIBRARIES IF MISSING
!pip install pyvis
!pip install requests
!pip install networkx

# Importing libraries
from pyvis.network import Network
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 25, 5

def transactions_graph(df):
    '''
    This function generates a transactions graph. 

    Parameters
    ----------
    df : Transactions data

    Returns
    -------
    None.

    '''
    df['Date'] = df['timestamp'].str[0:10]  # Extracting date from timestamp
    dfe = df.groupby(by='Date').count() # Grouping by date to find number of transactions per day
    dfe = dfe[['value']] # preprocessing dataframe
    dfe.columns = ['Number of transactions']# preprocessing dataframe
    dfe = dfe.reset_index()
    plt.plot(dfe.Date, dfe['Number of transactions'])  # Plot the chart 
    plt.title("Trustset transactions per day") #  Chart title
    plt.ylabel("Number of transactions")
    plt.xlabel("Date")
    plt.xticks(rotation=90) 
    plt.savefig(r"../Analysis/Trustset transactions per day.png") # Saving Chart
    dfe.to_excel(r"../Analysis/Trsuset_Transactions_per_day.xlsx", index=False) # Saving data

def check_change_in_trustset(df,account,issuer):
    '''
    This function outputs an average time in minutes at which trust is changing
    between 2 accounts mentioned.

    Parameters
    ----------
    df : Transactions data
    account : First wallet address
    issuer : Second wallet address

    Returns
    -------
    None.

    '''
    df = df[df["timestamp"]!="timestamp"] # Filtering Data
    df = df[(df["account"]==account) & (df["issuer"]==issuer)] # Extracting data with given account and issuer
    if df.shape[0]>1: # if there are more than one transactions between those 2 accounts
        df['timestamp'] = df['timestamp'].str.replace("T"," ") # Preprocessing timestamp column
        df['date'] = df['timestamp'].apply(lambda a: pd.to_datetime(a).date()) 
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by="timestamp", ascending =True)
        df = df.reset_index(drop=True)
        l=[]
        xs =df['timestamp'][0]
        for i in df['timestamp']: # getting minutes difference between two trustset transaction between account and issuer
            #l.append(i-xs)
            l.append(int(int((i-xs).seconds)/60)) # converting seconds to minutes.
            xs = i
        df["timediff from previous in minutes"] = l
        T = int(df["timediff from previous in minutes"].mean()) # getting average time in minutes between 2 transactions
        print("\n\nAverage time span between updating trust line between these 2 wallets is : "+str(T)+" Minutes")
    else:
        print("\n\nThere has been only one trustset Transaction between mentioned accounts")

def filter_transactions(df):
    '''
    This function filters the transaction data for latest transaction between 
    accounts to get the current state of network for creating a graph.

    Parameters
    ----------
    df : Transactions data

    Returns
    -------
    res_df : Filtered transactions data.

    '''
    df['timestamp'] = df['timestamp']
    df['tmp'] = df['account']+df['issuer'] # creating tmp column to get unique rows
    res_df = []
    for i in df['tmp'].unique():
        tmp_df = df.loc[df['tmp']==i] # fetch all transaction between account and issuer
        tmp_df = tmp_df.reset_index(drop=True) # reset index of fetched dataframe
        tmp_df = tmp_df.sort_values(by="timestamp",ascending=False) # sort data based on timestamp
        res_df.append(tmp_df.iloc[0]) # get latest trustline between account and issuer
    res_df = pd.DataFrame(res_df) # creating a result dataframe
    res_df.reset_index(inplace=True,drop=True) # resetting index
    res_df = res_df.drop("tmp",axis=1) # droppin unnecessary column
    return res_df

def generate_trustline_graph(data):
    '''
    This function generates a network graph using pyvis module. The graph is 
    saved in Analysis folder.

    Parameters
    ----------
    data : Filtered transactions data.

    Returns
    -------
    None.

    '''
    graphNodeList=[] # creating empty nodes list for graph
    for acc in data.index: # adding data to graph nodes list
        graphNodeList.append(data['account'][acc])  # appending account
        graphNodeList.append(data['issuer'][acc])   # appending issuer
    graphNodeList=list(set(graphNodeList)) # filtering graph node list for unique node list
    graphEdgeList=[] # create graph's edge list
    for acc in data.index: # adding data to graph's edges
        if(data['value'][acc]!=0): # don't add edge if trustline is set to 0
            graphEdgeList.append((data['account'][acc],data['issuer'][acc],data['currency'][acc],data['value'][acc])) # adding edge with account, issuer, currency and value   
    nx_graph =  Network(height="750px", width="100%", bgcolor="#222222", font_color="white",directed="true") # setting parameters for visualising the graph.
    for node in graphNodeList: # adding nodes to graph
        nx_graph.add_node(node, size=20, title=node)
    for edge in graphEdgeList: # adding edges to graph
        weigh= str(edge[3])+' '+str(edge[2])
        nx_graph.add_edge(edge[0], edge[1], weight=weigh, title=weigh) # adding edge with weights to graph
    neighbor_map = nx_graph.get_adj_list()
    for node in nx_graph.nodes:
        node["title"] += " Trusted:<br>" + "<br>".join(neighbor_map[node["id"]]) # creating title for each node
        node["value"] = len(neighbor_map[node["id"]]) # setting value of node
    nx_graph.save_graph(r"../Analysis/TrustSetGraph.html") # saving the graph in HTML format
    nx_graph.show_buttons(filter_=['physics']) 
    nx_graph.show("TrustSetGraph.html") # open the graph in browser


df = pd.read_csv(r"../Data/Data_jan2019_nov_2020.csv")  #   Read the transactions data
# df = df[df["timestamp"]!="timestamp"] # filter data for unnecessary rows.
# df.to_csv(r"../Data/Data_jan2019_nov_2020.csv", index=False)

transactions_graph(df)  #   generate a transactions per day graph


account="rGBg9FoDZcArRrubyoEyKrjwHSRBFj97Kg" # defining account value
issuer = "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL" # defining issuer value
check_change_in_trustset(df,account,issuer) # Get average time between trustset transactions between 2 wallets


res_df = filter_transactions(df) # This function filters the transaction data for latest transaction between accounts to get the current state of network for creating a graph. 
res_df.to_csv(r"../Data/filtered_transactions.csv", index=False) # Save the filtered transactions.


data=pd.read_csv(r"../Data/filtered_transactions.csv") # read the filtered transactions data
dfe = data.drop(["timestamp"], axis=1) # drop the unnecessary column
generate_trustline_graph(dfe) # This function generates a trustline graph.



dfe=pd.read_csv(r"../Data/Data_jan2019_nov_2020.csv") # read transactions data
G = nx.Graph() # generate networkx graph object
for i in range(0,dfe.shape[0]): # add nodes and edges to the graph.
    G.add_edge(dfe.account[i],dfe.issuer[i],weight = dfe.value[i],currency = dfe.currency[i])

                        # NETWORK METRICS
# Information of the Graph
print(nx.info(G)) # shows information about the graph 

'''
Density of the Graph
A good metric to begin with is network density. This is simply the ratio of 
actual edges in the network to all possible edges in the network.
'''
density = nx.density(G) # calulates density of graph
print("Network density:", density)


'''
Centrality
In network analysis, measures of the importance of nodes are referred to as 
centrality measures. Degree is the simplest and the most common way of 
finding important nodes. A node’s degree is the sum of its edges. If a node 
has three lines extending from it to other nodes, its degree is three. Five edges
'''
rsd = nx.degree_centrality(G) # calculates density of graph
rsdf = pd.DataFrame(pd.Series(rsd)) # preprocess the output 
rsdf = rsdf.reset_index() # reset the index
rsdf.columns = ["addresses","Degree centrality"] # renaming columns
rsdf = rsdf.sort_values(by="Degree centrality", ascending=False) # sorting based on descending centrality value
top_5_nodes = list(rsdf.addresses[0:5]) # get top 5 nodes
print(top_5_nodes) # print top 5 nodes


'''
Finding Diameter
Diameter is the longest of all shortest paths. After calculating all shortest
paths between every possible pair of nodes in the network, diameter is the 
length of the path between the two nodes that are furthest apart. The measure
is designed to give a sense of the network’s overall size, the distance from
one end of the network to another.
'''
# If your Graph has more than one component, this will return False:
print(nx.is_connected(G))
components = nx.connected_components(G) # using nx.connected_components to get the list of components
largest_component = max(components, key=len) # using the max() command to find the largest one
subgraph = G.subgraph(largest_component) # Create a "subgraph" of just the largest component
diameter = nx.diameter(subgraph) # Then calculate the diameter of the subgraph, just like you did with density.
print("Network diameter of largest component:", diameter) # print the diameter of graph


# Betweenness Centrality
betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
# Assign each to an attribute in your network
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
sorted_betweenness = sorted(betweenness_dict.items(), reverse=True)
print("Top 20 nodes by betweenness centrality:")
for b in sorted_betweenness[:20]: # print top 20 nodes by betweenness centrality
    print(b)


# Clustering Coefficient

G=G.to_undirected()
ccs=nx.clustering(G) # Clustering coefficient of all the nodes
average_ccs=sum(ccs.values())/len(ccs) # Average Clustering coefficient
print(average_ccs) # print the average clustering coefficient


# Eigenvector Centrality
G = nx.path_graph(10)
centrality = nx.eigenvector_centrality(G) # calculate the Eigenvector Centrality
print(['%s %0.2f'%(node,centrality[node]) for node in centrality])