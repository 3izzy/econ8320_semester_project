import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px


st.title("Welcome to my dashboard!")
st.subheader("Here you'll be able to 'play' with government data")
st.write("Each page is a different dataset and series from BLS")

st.sidebar.markdown("# Welcome page")
st.sidebar.markdown("Choose a page or play around here")


df_selection = st.selectbox("Choose a series",
                  ("Civilian Employment", 
                   "Civilian Unemployment", 
                   "Total Nonfarm Employment", 
                   "Unemployment Rate"))
df = pd.read_csv(f"data/{df_selection}.csv")
st.write(f"You chose: {df_selection}")
if st.checkbox("Show data:"):
    st.dataframe(df)
    

if st.checkbox("Show the line plot"):
    year_selection_line = st.multiselect("Select a year or more))) ", df['year'].unique(), key="line_year")
    month_selection_line = st.multiselect("Select months to display", df['month'].unique(), key="line_month")
    p = px.line(df[df["year"].isin(year_selection_line) & df["month"].isin(month_selection_line)], 
        x="month",
        y="value",
        color="year",
        category_orders={"month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
        ).update_layout(yaxis_title=df_selection)
    st.plotly_chart(p)
    
if st.checkbox("Show the histogram"):
    p2 = px.histogram(df,
                  x="value"
                  ).update_layout(xaxis_title=df_selection)
    st.plotly_chart(p2)
    
if st.checkbox("Show the bar chart"):
    year_selection_bar = st.multiselect("Select a year or more))) ", df['year'].unique(), key="bar_year")
    month_selection_bar = st.multiselect("Select months to display", df['month'].unique(), key="bar_month")
    temp_df = df.copy()
    temp_df['year'] = temp_df['year'].astype(str)
    st.write(temp_df.head())
    p3 = px.bar(temp_df[df["year"].isin(year_selection_bar) & df["month"].isin(month_selection_bar)], 
        x="month",
        y="value",
        color="year",
        barmode="group",
        category_orders={"month": ["January", "February", 
                                   "March", "April", "May", "June", 
                                   "July", "August", "September", "October", "November", "December"],
                         "year": [str(x) for x in df['year'].unique()]}
        ).update_layout(yaxis_title=df_selection, barmode='group')
    st.plotly_chart(p3)