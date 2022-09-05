"""
# My first app
Here's our first attempt at using data to create a table:
"""


import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d
from bokeh.models import HoverTool
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.themes import built_in_themes
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource
from plotly.subplots import make_subplots
import time




st.markdown(f'<h1 style="color:#02A4D3;font-size:40px;text-align:center;">{"Welcome to Snowflake Streamlit!"}</h1>', unsafe_allow_html=True)
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
       return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()


st.markdown(f'<h1 style="color:#33ff33;font-size:30px;text-align:center;">{"NYC Citibike Statistics"}</h1>', unsafe_allow_html=True)


df1=pd.read_sql_query('SELECT * FROM USAGE_BY_YR_MONTH',conn)
#st.dataframe(df1)

years = df1["YEAR"].drop_duplicates()
year_choice = st.sidebar.selectbox('Select Year', years) 
months = df1["MONTH"].loc[df1["YEAR"] == year_choice]
select_month_range = sorted(months.unique())
st.write(years)
st.write(year_choice)
st.write(months)
st.write(select_month_range)


select_month_slider = st.sidebar.select_slider('Use slider to display Month range:',select_month_range)
#months_choice = st.sidebar.selectbox('Select Month', months)
st.write('I have selected Months till ', select_month_slider, ' of Year ',year_choice)
numberoftrips = df1['NUMBER_OF_TRIPS'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
numberofbikes = df1['NUMBER_OF_BIKES'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
countfemale = df1['COUNT_FEMALE'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] == select_month_slider]
countmale = df1['COUNT_MALE'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] == select_month_slider]
df2 = df1.loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]

#st.write(numberoftrips)
#st.write(numberofbikes)



graph = figure(title = "Number of Trips per Month",width=450, height=350)

width = 0.5

graph.vbar(months,
top = numberoftrips,
width = width)
graph.add_tools(HoverTool(tooltips=[("Number of Trips","@top")]))



graph1 = figure(title = "Number of Bikes per Months",width=450, height=350)

width = 0.5

graph1.vbar(months,
top = numberofbikes,
width = width,color=Spectral6)
graph1.add_tools(HoverTool(tooltips=[("Number of Bikes","@top")]))
output_file("dark_minimal.html")
#st.bokeh_chart(graph, use_container_width=True)
st.bokeh_chart(row(graph, graph1))

#df2 = [months,numberoftrips]
#fig = px.bar(df2, x=months, y=numberoftrips)


st.snow()
#fig = make_subplots(rows=1, cols=2)

fig1 = px.bar(df2, x='MONTH', y='NUMBER_OF_TRIPS',
             title = "Number of Trips per Months",width=450, height=350)
fig2 = px.bar(df2, x='MONTH', y='NUMBER_OF_BIKES',
             title = "Number of Bikes per Months",width=450, height=350)

st.plotly_chart(fig1)
st.plotly_chart(fig2)

fig = make_subplots(rows=1, cols=2)
fig.add_trace(
    go.Bar(df2, x='MONTH', y='NUMBER_OF_TRIPS'),row=1, col=1)
#Second SubPlot
fig.add_trace(
    go.Bar(df2, x='MONTH', y='NUMBER_OF_BIKES'),row=1, col=1)
    
st.plotly_chart(fig)
