"""
# My first app
Here's our first attempt at using data to create a table:
"""


import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import altair as alt

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
st.title('NYC Citibike Station Explorer')
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from trips limit 10;")
df_pal = pd.read_sql_query('SELECT * from trips limit 10',conn)
print(df_pal)
station_info_query = """
    SELECT 
        *
    FROM  trips limit 10000;
"""

timeperiod_query = """
SELECT  
        min(starttime) as timeperiod_start,
        max(stoptime) as timeperiod_end
    FROM trips limit 10000;
"""

def generate_avg_trips_query(station_name):
    query =  f'''
    SELECT AVG(num_rides) as avg_num_rides FROM (
        SELECT  
            to_date(starttime) as date_part,
            count(bikeid) as num_rides
        FROM trips 
        WHERE start_station_name = "{station_name}"
        group by 1
    );
    
    '''
    return query

def generate_avg_trip_length_query(station_name):
    # warning, beware for long trips, may want to exclude
    query =  f'''
        SELECT  
            avg(
                ((to_date(stoptime) - to_date(starttime)) * (60*24)) +
                ((hour(stoptime) - hour(starttime)) * 60) +
                (MINUTE(stoptime) - MINUTE(starttime)) +
                ((SECOND(stoptime) - SECOND(starttime)) / 60)
            )
        FROM trips 
        WHERE start_station_name = "{station_name}"
        and end_station_name is not null
    '''
    return query

def generate_top_destinations_query(station_name):
    query = f'''
    with station_destination_df as (
        SELECT  
            end_station_name,
            bikeid,
            (
                ((to_date(stoptime) - to_date(starttime)) * (60*24)) +
                ((hour(stoptime) - hour(starttime)) * 60) +
                (MINUTE(stoptime) - MINUTE(starttime)) +
                ((SECOND(stoptime) - SECOND(starttime)) / 60)
            ) as trip_length_minutes
        FROM trips 
        WHERE start_station_name = "{station_name}"
        and end_station_name is not null
    )
    select 
        end_station_name,
        count(bikeid) as num_rides,
        count(bikeid) / (select count(bikeid) from station_destination_df) as pct_total_rides,
        avg(trip_length_minutes) as avg_trip_length
    from station_destination_df 
    group by 1
    order by 2 desc
    limit 20
    '''
    return query

def generate_num_rides_by_hour_query(station_name):
    query = f'''
        SELECT 
            hour,
            num_rides / (select (max (to_date(starttime)) - min(to_date(stoptime))) ) as num_days
            FROM trips 
            WHERE start_station_name = "{station_name}"
            and end_station_name is not null) as daily_avg
        from (
        SELECT  
            HOUR(starttime) AS hour,
            count(bikeid) as num_rides,
        FROM trips 
        WHERE start_station_name = "{station_name}"
        and end_station_name is not null
        group by 1
        )
        order by 1
    '''
    return query

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
    
# Uses st.cache to only rerun when the query changes or after 15 min.






## INITIAL DATA LOAD ##

station_info_df = run_query(station_info_query)
print(station_info_df)
timeperiod_df = run_query(timeperiod_query)

### UI CODE ###

st.title('NYC Citibike Station Explorer')
timeperiod_start = timeperiod_df.iloc[0][0]
timeperiod_end = timeperiod_df.iloc[0][1]
timeperiod_num_days= (timeperiod_end.date() - timeperiod_start.date()).days
st.write(f'Data for {timeperiod_start.date()} through {timeperiod_end.date()}')
# specify station
station_col1, station_col2, station_col3 = st.columns(3)

with station_col1:
    borough_list = np.sort(station_info_df['borough'].unique())
    borough = st.selectbox(
        label='Select Borough',
        options=borough_list
    )      
with station_col2:
    neighborhood_list = np.sort(
        station_info_df \
            .loc[station_info_df['borough']==borough]['neighborhood'].unique()
    )
    neighborhood = st.selectbox(
        label='Select Neighborhood',
        options=neighborhood_list
    )      
with station_col3:
    station_list = np.sort(
        station_info_df \
            .loc[(station_info_df['borough']==borough) \
                & (station_info_df['neighborhood']==neighborhood)] \
            ['station_name'].unique()
    )
    station = st.selectbox(
        label='Select Station',
        options=station_list
    )      



main_col1, main_col2 = st.columns(2)

with main_col2:
    
    num_rides_by_hour_query = generate_num_rides_by_hour_query(station)
    num_rides_by_hour_df = run_query(num_rides_by_hour_query)
    '''num_rides_by_hour_hist = go.Figure(
        go.Bar(
            x=pd.to_datetime(num_rides_by_hour_df['hour'], format='%H').dt.time, 
            y=num_rides_by_hour_df['daily_avg']
        )
    )
    num_rides_by_hour_hist.update_layout(
        title='Hourly Ride Distribution',
        yaxis_title='# Trips (daily avg.)',
        xaxis_title='Time of Day',
        title_font=dict(
            size=24
        )
    )'''

    #st.plotly_chart(num_rides_by_hour_hist)
    st.dataframe(num_rides_by_hour_df)
    st.altair_chart(alt.Chart(num_rides_by_hour_df, height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))

# To Do organize queries, add better search to the station finder
