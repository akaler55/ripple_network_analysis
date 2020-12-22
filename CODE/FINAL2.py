# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:37:37 2020

@author: UofM
"""
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 25, 5

def transactions_graph(df):
    df['Date'] = df['timestamp'].str[0:10]
    dfe = df.groupby(by='Date').count()
    dfe = dfe[['value']]
    dfe.columns = ['Number of transactions']
    dfe = dfe.reset_index()
    plt.plot(dfe.Date, dfe['Number of transactions'])  # Plot the chart 
    plt.title("Trustset transactions per day")
    plt.ylabel("Number of transactions")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.savefig(r"../Analysis/Trustset transactions per day.png")
    dfe.to_excel(r"../Analysis/Trsuset_Transactions_per_day.xlsx", index=False)

def check_change_in_trustset(df,account,issuer):
    df = df[df["timestamp"]!="timestamp"]
    df = df[(df["account"]==account) & (df["issuer"]==issuer)]
    if df.shape[0]>1:
        df['timestamp'] = df['timestamp'].str.replace("T"," ")
        df['date'] = df['timestamp'].apply(lambda a: pd.to_datetime(a).date()) 
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by="timestamp", ascending =True)
        df = df.reset_index(drop=True)
        l=[]
        xs =df['timestamp'][0]
        for i in df['timestamp']:
            #l.append(i-xs)
            l.append(int(int((i-xs).seconds)/60))
            xs = i
        df["timediff from previous in minutes"] = l
        T = int(df["timediff from previous in minutes"].mean())
        print("\n\nAverage time span between updating trustset is : "+str(T)+" Minutes")
    else:
        print("\n\nThere has been only one trustset Transaction between mentioned accounts")



df = pd.read_csv(r"../Data/Data_jan2019_nov_2020.csv")
df = df[df["timestamp"]!="timestamp"]
df.to_csv("Data_jan2019_nov_2020.csv", index=False)

transactions_graph(df) 

account="rGBg9FoDZcArRrubyoEyKrjwHSRBFj97Kg"
issuer = "rchGBxcD1A1C2tdxF6papQYZ8kjRKMYcL"
check_change_in_trustset(df,account,issuer)

   
