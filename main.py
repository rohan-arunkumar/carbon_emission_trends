import streamlit as st 

img_url = "carbonbanner.jpg"
st.image(img_url, caption="Vehicle Pollution")
st.title("Carbon Emission Trends")
st.header("Information")
st.write("""The largest factors for CO2 emissions:
1. Fuel Type
2. Engine Size""")