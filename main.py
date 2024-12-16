import requests
import json
import prettytable
import pandas as pd
import numpy as np
import streamlit as st
import os



#### to create original datasets
def get_datasets():
    all_series = pd.read_csv("series.csv")
    all_series_list = (list(all_series.iloc[:,0]))
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": all_series_list,"startyear":"2023", "endyear":"2024"})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    #create a folder if it's missing
    outdir = "./data/"
    if not os.path.exists(outdir):
        os.mkdir(outdir)


    for series in json_data['Results']['series']:
        outname = str(all_series.loc[all_series['Series_id'] == series['seriesID'], "Series_name"].item()).strip() + ".csv".strip()
        fullname = os.path.join(outdir, outname)
        df = pd.DataFrame(series['data'])
        #df['labs'] = [str(x)+" "+y if y=="January" else y for _,(x,y) in enumerate(zip(df['year'], df['periodName'])) ]
        df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
        df['month'] = pd.to_datetime(df['periodName'], format='%B').dt.month_name()
        df.drop('periodName', axis=1, inplace=True)
        df = df[['year','month','period','value','footnotes','latest']]
        df.to_csv(fullname, index=False)
    pass
 
 ### initialize a page intro 
def get_data_intro():
    file_name_list = os.path.basename(__file__)[2:-3].split("_")
    file_name = file_name_list[0] + " " + file_name_list[1]
    st.markdown(f"# {file_name}")
    st.sidebar.markdown(f"# {file_name}")

    df = pd.read_csv(f"data/{file_name}.csv")
    df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
    df['month'] = pd.to_datetime(df['month'], format='%B').dt.month_name()
    pass
 
def is_not_number(s):
    try:
        float(s)
        return False
    except ValueError:
        return True

get_datasets()

#df['labs'] = [str(x)+" "+y if y=="January" else y for _,(x,y) in enumerate(zip(df['year'], df['periodName'])) ]

st.write(os.path.basename(__file__))