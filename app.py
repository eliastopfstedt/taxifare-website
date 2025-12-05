import streamlit as st
import pandas as pd
from datetime import *
import requests

'''
# TaxiFare AI

## *Predict taxi fares for NYC the easy way*
'''

# Inputs
ride_date = st.date_input("Date of the ride", value=datetime.today())
ride_time = st.time_input("Time of the ride", value=datetime.now().time())

pickup_latitude = st.number_input('Insert pickup latitude',format="%0.3f", step=0.001, value=40.779)
pickup_longitude = st.number_input('Insert pickup longitude',format="%0.3f", step=0.001, value=-73.963)
dropoff_latitude = st.number_input('Insert dropoff latitude',format="%0.3f", step=0.001, value=40.725)
dropoff_longitude = st.number_input('Insert dropoff longitude',format="%0.3f", step=0.001, value=-73.996)

passenger_count = st.number_input("Passenger Count", min_value=1, max_value=10, value=1)

def get_map_data(
    pickup_latitude=40.779,
    pickup_longitude=-73.963,
    dropoff_latitude=40.725,
    dropoff_longitude=-73.996):
    # Metropolitan Museum of Art (pickup) and JFK Airport (dropoff)
    return pd.DataFrame(
        [
            [pickup_latitude, pickup_longitude, "#2f00fe"],  # Metropolitan Museum of Art (Manhattan)
            [dropoff_latitude, dropoff_longitude, "#ff0040"]   # Brooklyn Bridge (Brooklyn)
        ],
        columns=['lat', 'lon', 'color']
    )

df = get_map_data(
    pickup_latitude=pickup_latitude,
    pickup_longitude=pickup_longitude,
    dropoff_latitude=dropoff_latitude,
    dropoff_longitude=dropoff_longitude
    )

st.map(df, latitude='lat', longitude='lon', color='color')
st.markdown("""
🔵 Pickup Location
🔴 Dropoff Location
######
""")

url = 'https://taxifare.lewagon.ai/predict'

if st.button("Get Fare Estimate"):
    if pickup_latitude and pickup_longitude and dropoff_latitude and dropoff_longitude:
        pickup_datetime = f"{ride_date}T{ride_time.strftime('%H:%M:%S')}"

        params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            prediction = response.json().get("fare")
            st.success(f'The estimated fare is: ${prediction:.2f}')
            st.snow()
        else:
            st.error("Error: Unable to retrieve the fare. Please check your inputs.")
    else:
        st.warning("Please enter valid pickup and dropoff locations.")
