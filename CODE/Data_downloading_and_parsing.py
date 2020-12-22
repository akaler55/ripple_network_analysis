# -*- coding: utf-8 -*-
"""
@author: Amandeep Singh, Rahul
"""

'''
This Program fetches the Ripple network data from API ("https://data.ripple.com/")
 for Trsutset transactions for the specified start and end dates. It extracts, 
 Parse and store data in csv format for using it in further analysis.
'''

import requests
import pandas as pd
import time
import sys
import json

# EXTRACTING START AND END DATES FOR DATA FETCHING
sdate = str(sys.argv[1])
edate = str(sys.argv[2])

# start_date= "2019-01-01"
# end_date = "2019-01-07"

start_date= sdate # START DATE
end_date = edate  # END DATE
print("\n\nData Fetching Start Date: "+start_date)
print("Data Fetching End Date: "+end_date)

# CREATING TEMPORARY VARIABLES FOR USING IT NEXT PARTS
a = start_date 
b = end_date 
rs_l=[]
t1 = pd.to_datetime(start_date) + pd.DateOffset(days=5)
t1 = pd.to_datetime(t1,unit='D')
t2 = str(t1.date())
y = t2
seq = ["Fetching Data from: "+str(a)+"   :    "+str(b)]


# While loop to fetch the data until we reaches end date, while using a subset of 5 days for each iteration
while pd.to_datetime(end_date)>pd.to_datetime(y):
    x = start_date #Start date
    y = t2 # Start date
    
    #Parameters used while sending request to API for fetching the data
    query_params = {}
    query_params["type"] = "TrustSet"
    query_params["result"] = "tesSUCCESS"
    #query_params["start"] = "2015-08-01T01:00"
    #query_params["end"] = "2015-08-01T23:00"
    query_params["start"] = x
    query_params["end"] = y
    query_params["limit"] = 100
    

    c=True
    rs_l=[]
    while(c==True):
        r=requests.get("http://data.ripple.com/v2/transactions",params=query_params) #Sending request to API with query parameters for trustset transactions
        #print(str(r))
        if not("200" in str(r)):# If request returns any other response than 200("successful") then show error
            print(str(r))
            seq.append("\n.............ERROR...............  skipped       "+str(x)+"---"+str(y)+"\n") 
            print(".............ERROR...............")
            c = False
            break
        
        rd = r.json()
        file1 = open(r"../Data/Raw_JSON_data.txt", "a")  # Writing data file with raw format data fetched from request 
        file1.write(json.dumps(rd)) 
        file1.close()
        rs_l.append(rd)
        try: # Updating marker used for pagination it points to next page as in request we only get 100 requests
            query_params['marker'] = rd['marker']
            time.sleep(7)
        except: # if all the pages are fetched for particular dates then run this block
            c=False
            print("\n"+ x +"complete data fetched" + y+"\n")
            seq.append("\n"+ str(x) +"complete data fetched" + str(y)+"\n")
            
    print("Number of pages Fetched  : " +str(len(rs_l)))
    seq.append("Number of pages Fetched  : " +str(len(rs_l)))
    
    # Parsing data into CSV file from raw JSON format. Extracting details from JSON format.
    result_list=[]
    try:
        for i in range(0,len(rs_l)):
            result_set = rs_l[i]
            result_set_txs = result_set['transactions']
            for j in range(0,len(result_set_txs)):
                tx = result_set_txs[j]
                timestamp = tx['date']
                tx_details = tx['tx']
                account = tx_details['Account']
                value = tx_details['LimitAmount']['value']
                currency = tx_details['LimitAmount']['currency']
                issuer = tx_details['LimitAmount']['issuer']
                lsde = {}
                # Populating Columns for CSV Timestamp,account, issuer, currency, value 
                lsde['timestamp'] = timestamp
                lsde['account'] = account
                lsde['issuer'] = issuer
                lsde['currency'] = currency
                lsde['value'] = value
                result_list.append(lsde)
        df = pd.DataFrame(result_list)
        df.to_csv(r"../Data/Parsed_fetched_data.csv",mode='a', index=False) # Appending fetched data to CSV file.

    except: # if any error occur in the parsing block of code
        print("..................Error occured in parsing the data!!!!..................")
    
    # Updating the start date and end date to next 5 days
    t1 = pd.to_datetime(y) + pd.DateOffset(days=1) # Start Date next date to end date
    t1 = pd.to_datetime(t1,unit='D')
    t2 = str(t1.date())
    start_date = t2
    t1 = pd.to_datetime(start_date) + pd.DateOffset(days=5) # end date updated with next 5 days
    if t1<=pd.to_datetime(end_date):
        t1 = pd.to_datetime(t1,unit='D')
        t2 = str(t1.date())
    else:
        t2 = end_date

print("Number of pages Fetched  : " +str(len(rs_l))) # Total 

# Writing Logs of Dates and number of pages fetched 
file = open(r"LOGS data downloading and parsing.txt", "w") 
seq.append("\n\nFetching Data from: "+str(a)+"   :    "+str(b)+" \nThe data fetching Stopped at :"+str(x)+"\n Resume from :"+str(x)) 
file.writelines(seq)
file.close()

# Removing any duplicates entries in the Final Output file
df = pd.read_csv(r"../Data/Parsed_fetched_data.csv")
df = df[df["timestamp"]!="timestamp"]
df = df.drop_duplicates()
df.to_csv(r"../Data/final_Parsed_fetched_data.csv", index=False)