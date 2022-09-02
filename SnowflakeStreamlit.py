"""
# My first app
Here's our first attempt at using data to create a table:
"""


import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import altair as alt
from bokeh.plotting import figure, output_file, show
"""
# Welcome to Snowflake Streamlit!
# # THINK BIG :heart:
"""

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
st.title('NYC Citibike Statistics')
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,conn)
    
    return df

rows = run_query("SELECT * from trips limit 10;")
df_pal = pd.read_sql_query('SELECT * from trips limit 10',conn)
st.dataframe(df_pal)

df1=pd.read_sql_query('SELECT * FROM USAGE_BY_GENDER',conn)

source = df1

# importing the modules


# file to save the model
output_file("gfg.html")
	
# instantiating the figure object
graph = figure(title = "Bokeh Vertical Bar Graph")


# width / thickness of the bars
width = 0.5

# plotting the graph
graph.vbar(df1.YEAR,
top = df1.FEMALE,
width = width)

# displaying the model
#st.show(graph)
st.bokeh_chart(graph, use_container_width=True)
