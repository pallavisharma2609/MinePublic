
import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots





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
year_choice = st.sidebar.selectbox('Select Year', years,value=2017) 
months = df1["MONTH"].loc[df1["YEAR"] == year_choice]
select_month_range = sorted(months.unique())



select_month_slider = st.sidebar.select_slider('Use slider to display Month range:',select_month_range,value=6)
#months_choice = st.sidebar.selectbox('Select Month', months)
st.write('I have selected Months till ', select_month_slider, ' of Year ',year_choice)
numberoftrips = df1['NUMBER_OF_TRIPS'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
numberofbikes = df1['NUMBER_OF_BIKES'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
countfemale = df1['COUNT_FEMALE'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
countmale = df1['COUNT_MALE'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
count_subscriber=df1['COUNT_SUBSCRIBER'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]
count_customer=df1['COUNT_CUSTOMER'].loc[df1["YEAR"] == year_choice].loc[df1["MONTH"] <= select_month_slider]


@st.cache(suppress_st_warning=True)
def bind_socket():
    # This function will only be run the first time it's called
    st.snow()

bind_socket()

#fig = make_subplots(rows=1, cols=2)


fig = make_subplots(rows=1, cols=2,subplot_titles=("Number of Trips per Month", "Number of Bikes per Month"))
fig.add_trace(
    go.Bar( x=months, y=numberoftrips,marker=dict(color=numberoftrips, coloraxis="coloraxis")),row=1, col=1)
#Second SubPlot
fig.add_trace(
    go.Bar(x=months, y=numberofbikes,marker=dict(color=numberofbikes, coloraxis="coloraxis")),row=1, col=2)
 
fig.update_layout(autosize=True,coloraxis=dict(colorscale='Emrld'), showlegend=False,margin=dict(l=20, r=20, t=20, b=20))   
st.plotly_chart(fig)



fig1 = make_subplots(rows=1, cols=2,subplot_titles=("Number of Trips (Female) per Month", "Number of Trips (Male) per Month"))
fig1.add_trace(
    go.Bar( x=months, y=count_subscriber,marker=dict(color=count_subscriber, coloraxis="coloraxis")),row=1, col=1)
#Second SubPlot
fig1.add_trace(
    go.Bar(x=months, y=countmale,marker=dict(color=countmale, coloraxis="coloraxis")),row=1, col=2)
 
fig1.update_layout(autosize=True,coloraxis=dict(colorscale='YlGnBu'), showlegend=False,margin=dict(l=20, r=20, t=20, b=20))   
st.plotly_chart(fig1)

fig2 = make_subplots(rows=1, cols=2,subplot_titles=("Number of Subscribers per Month", "Number of Customers per Month"))
fig2.add_trace(
    go.Bar( x=months, y=countfemale,marker=dict(color=countfemale, coloraxis="coloraxis")),row=1, col=1)
#Second SubPlot
fig2.add_trace(
    go.Bar(x=months, y=count_customer,marker=dict(color=count_customer, coloraxis="coloraxis")),row=1, col=2)
 
fig2.update_layout(autosize=True,coloraxis=dict(colorscale='dense'), showlegend=False,margin=dict(l=20, r=20, t=20, b=20))   
st.plotly_chart(fig2)

