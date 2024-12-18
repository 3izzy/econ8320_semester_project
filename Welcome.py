import pandas as pd
import numpy as np
import streamlit as st
import os


st.title("Welcome to my dashboard!")
st.subheader("Here you'll be able to 'play' with government data")
st.write("Each page is a different dataset and series from BLS")

st.sidebar.markdown("# Welcome page")
st.sidebar.markdown("Choose a page")
