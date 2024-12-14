import streamlit as st
import pickle 
from PIL import Image

img_url = "carbonbanner.jpg"
image = Image.open(img_url)
st.image(image, caption="Vehicle Pollution")
st.title("Carbon Emission Trends")
st.header("Information")
st.write("""The largest factors for CO2 emissions:
1. Fuel Type
2. Engine Size""")

st.header("Predict Using AI")

# loading in the model to predict on the data
pickle_in = open('best_model_MLP_subset1.pkl', 'rb')
classifier = pickle.load(pickle_in)

fuel_type = st.text_input("Fuel Type", "Type Here")
engine_size = st.text_input("Engine Size", "Type Here")
cylinders = st.text_input("Cylinders", "Type Here")
transmission = st.text_input("Transmission", "Type Here")
fuel_consumption_city = st.text_input("Fuel Consumption City (L/100 km)", "Type Here")
fuel_consumption_hwy = st.text_input("Fuel Consumption Hwy (L/100 km)", "Type Here")
fuel_consumption_combL = st.text_input("Fuel Consumption Comb (L/100 km)", "Type Here")
fuel_consumption_combG = st.text_input("Fuel Consumption Comb (mpg)", "Type Here")


if st.button("Predict"):
    result = prediction(fuel_type, engine_size, cylinders, transmission, fuel_consumption_city, fuel_consumption_hwy, fuel_consumption_combL, fuel_consumption_combG)
    st.success('The output is {}'.format(result))

