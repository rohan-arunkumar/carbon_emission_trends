import streamlit as st 

img_url = "https://media.istockphoto.com/id/1254838231/vector/cars-air-pollution-polluted-air-environment-at-city-vehicle-traffic-and-toxic-pollution-car.jpg"
st.image(img_url, caption="Vehicle Pollution")
st.title("Carbon Emission Trends")
st.header("Information")
st.write("""The largest factors for CO2 emissions:
1. Fuel Type
2. Engine Size""")