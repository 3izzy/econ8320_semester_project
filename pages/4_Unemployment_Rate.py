import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px
from main import is_not_number



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


st.markdown("Data measured in thousands")

st.markdown("## Visualizations")
### VISUALIZATION OF DATA
p = px.line(df, 
        x="month",
        y="value",
        color="year",
        category_orders={"month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
        ).update_layout(yaxis_title=file_name)

p2 = px.histogram(df,
                  x="value")

st.markdown(f"#### How {file_name} changes overtime")
st.plotly_chart(p)
st.markdown(f'#### Distribution of {file_name}')
st.plotly_chart(p2)
