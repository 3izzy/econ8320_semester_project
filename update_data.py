import requests
import json
import pandas as pd
import os
import datetime




#### download datasets and append to the existing ones
def update_datasets():
    all_series = pd.read_csv("series.csv")
    all_series_list = (list(all_series.iloc[:,0]))
    headers = {'Content-type': 'application/json'}
    cur_year = datetime.datetime.now().year
    data = json.dumps({"seriesid": all_series_list,"startyear":str(cur_year), "endyear":str(cur_year)})
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
        df['latest'] = df['latest'].notnull()
        df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
        df['month'] = pd.to_datetime(df['periodName'], format='%B').dt.month_name()
        df.drop('periodName', axis=1, inplace=True)
        df = df[['year','month','period','value','footnotes','latest']]
        df.loc[df['latest'] == True].to_csv(fullname, index=False, mode="a", header=False)
    pass
 
 
 
update_datasets()


