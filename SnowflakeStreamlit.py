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
from bokeh.models import Range1d
from bokeh.models import HoverTool
from bokeh.io import curdoc
from bokeh.themes import built_in_themes

"""
# Welcome to Snowflake Streamlit!
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

#rows = run_query("SELECT * from trips limit 10;")
#df_pal = pd.read_sql_query('SELECT * from trips limit 10',conn)
#st.dataframe(df_pal)

df1=pd.read_sql_query('SELECT * FROM USAGE_BY_YR_MONTH',conn)

#source = df1

# importing the modules


#year_choice ='2018'
#months_choice='13'
years = df1["YEAR"].drop_duplicates()
year_choice = st.sidebar.selectbox('Select Year', years) 
months = df1["MONTH"].loc[df1["YEAR"] == year_choice]
#months_choice = st.sidebar.selectbox('Select Month', months)
numberoftrips = df1['NUMBER_OF_TRIPS'].loc[df1["YEAR"] == year_choice]





# file to save the model
#output_file("gfg.html")
output_file("dark_minimal.html")
#curdoc().theme = 'caliber'	
# instantiating the figure object
graph = figure(title = "Number of Trips per Month")

curdoc().theme = 'dark_minimal'
# width / thickness of the bars
width = 0.5
#graph.y_range = Range1d(150000, 2053052)
# plotting the graph
graph.vbar(months,
top = numberoftrips,
width = width)
graph.add_tools(HoverTool(tooltips=[("Number of Trips","@top")]))
# displaying the model
#st.show(graph)
st.bokeh_chart(graph, use_container_width=True)
