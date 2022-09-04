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
from bokeh.layouts import row
from bokeh.themes import built_in_themes
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource
from bokeh.transform import cumsum
import time




st.markdown(f'<h1 style="color:#02A4D3;font-size:40px;text-align:center;">{"Welcome to Snowflake Streamlit!"}</h1>', unsafe_allow_html=True)
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
       return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.style='text-align: center;
#st.title('NYC Citibike Statistics')
st.markdown(f'<h1 style="color:#33ff33;font-size:30px;text-align:center;">{"NYC Citibike Statistics"}</h1>', unsafe_allow_html=True)
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
select_month_range = sorted(months.unique())

select_month_slider = st.sidebar.select_slider('Use slider to display Month range:',select_month_range)
#months_choice = st.sidebar.selectbox('Select Month', months)
st.write('I have selected Months till ', select_month_slider, ' of Year ',year_choice)
numberoftrips = df1['NUMBER_OF_TRIPS'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
numberofbikes = df1['NUMBER_OF_BIKES'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
countfemale = df1['COUNT_FEMALE'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
countmale = df1['COUNT_MALE'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]


output_file("dark_minimal.html")

graph = figure(title = "Number of Trips per Month",width=450, height=350)

width = 0.5

graph.vbar(months,
top = numberoftrips,
width = width)
graph.add_tools(HoverTool(tooltips=[("Number of Trips","@top")]))

#st.markdown(f'<h1 style="color:#ffd700;font-size:18px;">{"Number of Trips per Month"}</h1>', unsafe_allow_html=True)

graph1 = figure(title = "Number of Bikes per Months",width=450, height=350)

width = 0.5

graph1.vbar(months,
top = numberofbikes,
width = width,color=Spectral6)
graph1.add_tools(HoverTool(tooltips=[("Number of Bikes","@top")]))
#st.bokeh_chart(graph, use_container_width=True)
st.bokeh_chart(row(graph, graph1))


output_file("gfg.html") 
           
# instantiating the figure object 
graph2 = figure(title = "Usage by Gender") 
  
 
# radius of the glyphs
radius = 0.4
# plotting the graph
graph2.wedge(countfemale, countmale, radius,start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'))
  
# displaying the graph
st.bokeh_chart(graph2)
st.snow()
