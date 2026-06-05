import pandas as pd
import requests
import json
schemes = {
    "HDFC_top_100":125497 ,
    "SBI_Bluechip":119551 ,
    "ICICI_Bluechip":120503,
    "Nippon_Large_Cap":118632,
    "Axis_Bluechip":119092,
    "Kotak_Bluechip":120841} # put All the value in key-value pair dict so its easy to acceses and makw it easy
# to access
schemes.items()
all_df=[]
for scheme_name,amfi_code in schemes.items():
    url=f"https://api.mfapi.in/mf/{amfi_code}"
    respond=requests.get(url)
        
    data=respond.json()
    df=pd.DataFrame(data['data'])

    # add there amfi code which is same and scheme name which is also same 
    df["amfi_code"]=amfi_code
    df["scheme_name"]=scheme_name

    #  add to combine it
    all_df.append(df)

    conc_df=pd.concat(all_df,ignore_index=True)


conc_df.to_csv(r"C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics\data\raw\Nav_fetch_data.csv",index=False)