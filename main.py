import streamlit as st 
from PIL import Image

img_url = "carbonbanner.jpg"
image = Image.open(image_url)
st.image(image, caption="Vehicle Pollution")
st.title("Carbon Emission Trends")
st.header("Information")
st.write("""The largest factors for CO2 emissions:
1. Fuel Type
2. Engine Size""")