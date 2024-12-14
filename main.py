import streamlit as st
import pickle 
from PIL import Image

# loading in the model to predict on the data
pickle_in = open('best_model_MLP_subset1.pkl', 'rb')
classifier = pickle.load(pickle_in)

Fuel_type = st.text_input("Fuel Type", "Type Here")
Fuel_type = st.text_input("Fuel Type", "Type Here")
Fuel_type = st.text_input("Fuel Type", "Type Here")
Fuel_type = st.text_input("Fuel Type", "Type Here")
Fuel_type = st.text_input("Fuel Type", "Type Here")
Fuel_type = st.text_input("Fuel Type", "Type Here")

if st.button("Predict"):
    result = prediction(sepal_length, sepal_width, petal_length, petal_width)
    st.success('The output is {}'.format(result))


img_url = "carbonbanner.jpg"
image = Image.open(img_url)
st.image(image, caption="Vehicle Pollution")
st.title("Carbon Emission Trends")
st.header("Information")
st.write("""The largest factors for CO2 emissions:
1. Fuel Type
2. Engine Size""")
