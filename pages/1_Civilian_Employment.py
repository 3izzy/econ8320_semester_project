import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px
from main import get_data_intro, is_not_number



file_name_list = os.path.basename(__file__).split("_")
file_name_list = [x[:-3] if x[-3:]==".py" else x for x in file_name_list]
file_name = " ".join(x for x in file_name_list if is_not_number(x))

st.markdown(f"# {file_name}")
st.sidebar.markdown(f"# {file_name}")

df = pd.read_csv(f"data/{file_name}.csv")
df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
df['month'] = pd.to_datetime(df['month'], format='%B').dt.month_name()

### DATA PREVIEW WITH AN OPTION
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df)




### VISUALIZATION OF DATA
p = px.line(df, 
        x="month",
        y="value",
        color="year",
        category_orders={"month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
        ).update_layout(yaxis_title=file_name)


st.plotly_chart(p)






multi = """Few things I've picked up from this plot:  
* similar pattern of the line for both years  
* the rate of increase of the slope was bigger in 2023 than in 2024  
* overall the levels have almost converged  
* the overall deviation visually is within 1,000 workers"""
st.markdown(multi)








