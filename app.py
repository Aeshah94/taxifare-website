import streamlit as st
import requests
import pandas as pd

# Main Title
st.title("🚖 Taxi Fare Prediction App")

# Introduction Section
st.markdown("""
This app allows you to input ride details and get a **predicted taxi fare** using a machine learning model.
Simply fill in the details below and hit the "Get Fare Prediction" button.
""")

# Input parameters for the ride
st.header("📋 Input Ride Parameters")

st.markdown("### Select the ride details:")

# Create columns for date and time
col1, col2 = st.columns(2)
with col1:
    date_time = st.date_input("Select Date", value=pd.to_datetime("today").date())
with col2:
    time_input = st.time_input("Select Time", value=pd.to_datetime("now").time())

# Create columns for pickup and dropoff coordinates
st.markdown("### Enter the coordinates:")
col3, col4 = st.columns(2)
with col3:
    pickup_longitude = st.number_input("Pickup Longitude", value=-73.950655, format="%f")
    pickup_latitude = st.number_input("Pickup Latitude", value=40.783282, format="%f")
with col4:
    dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.984365, format="%f")
    dropoff_latitude = st.number_input("Dropoff Latitude", value=40.769802, format="%f")

# Passenger count input
st.markdown("### Select number of passengers:")
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6, value=1)

# API Section
st.markdown("---")  # Divider
st.subheader("🚀 Get Fare Prediction")

st.markdown("""
Once you've entered the ride details, click the button below to retrieve the predicted fare:
""")

# Update the URL to point to the `/predict` endpoint
url = 'https://wagon-data-tpl-image-997933156872.europe-west1.run.app/predict'

# Build a dictionary for the API parameters
params = {
    "pickup_datetime": f"{date_time} {time_input}",
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# Call the API and display the result
if st.button("💰 Get Fare Prediction"):
    response = requests.get(url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        try:
            prediction = response.json().get("fare", None)
            if prediction is not None:
                st.success(f"🎉 The predicted fare is: **${prediction:.2f}**")
            else:
                st.error("⚠️ The response did not contain a 'fare' key. Here's the full response:")
                st.json(response.json())  # Print full response for debugging
        except Exception as e:
            st.error(f"⚠️ Error parsing the response: {e}")
    else:
        st.error(f"⚠️ Error retrieving the prediction. Status code: {response.status_code}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Aeshah")
