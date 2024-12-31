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

input_columns = [
    'Engine Size(L)', 'Cylinders', 'Fuel Consumption City (L/100 km)',
    'Fuel Consumption Hwy (L/100 km)', 'Fuel Consumption Comb (L/100 km)',
    'Fuel Consumption Comb (mpg)', 'Transmission_A10', 'Transmission_A4',
    'Transmission_A5', 'Transmission_A6', 'Transmission_A7', 'Transmission_A8',
    'Transmission_A9', 'Transmission_AM5', 'Transmission_AM6',
    'Transmission_AM7', 'Transmission_AM8', 'Transmission_AM9',
    'Transmission_AS10', 'Transmission_AS4', 'Transmission_AS5',
    'Transmission_AS6', 'Transmission_AS7', 'Transmission_AS8',
    'Transmission_AS9', 'Transmission_AV', 'Transmission_AV10',
    'Transmission_AV6', 'Transmission_AV7', 'Transmission_AV8',
    'Transmission_M5', 'Transmission_M6', 'Transmission_M7', 'Fuel Type_D',
    'Fuel Type_E', 'Fuel Type_X', 'Fuel Type_Z'
]

def process_car_input(user_input):
    """
    Process user input to generate the final list with one-hot encoding for Transmission and Fuel Type.

    :param user_input: A dictionary with user-provided car information.
    :return: A list representing the processed input.
    """
    # Initialize the output list with zeros
    output_list = [0] * len(input_columns)

    for key, value in user_input.items():
        if key in input_columns:
            # For numerical fields, directly assign the value
            output_list[input_columns.index(key)] = value
        elif key == "Transmission":
            # Handle Transmission one-hot encoding
            transmission_column = f"Transmission_{value}"
            if transmission_column in input_columns:
                output_list[input_columns.index(transmission_column)] = 1
        elif key == "Fuel Type":
            # Handle Fuel Type one-hot encoding
            fuel_type_column = f"Fuel Type_{value}"
            if fuel_type_column in input_columns:
                output_list[input_columns.index(fuel_type_column)] = 1

    return output_list

# Example usage
user_input = {
    "Engine Size(L)": engine_size,
    "Cylinders": cylinders,
    "Fuel Consumption City (L/100 km)": fuel_consumption_city,
    "Fuel Consumption Hwy (L/100 km)": fuel_consumption_hwy,
    "Fuel Consumption Comb (L/100 km)": fuel_consumption_combL,
    "Fuel Consumption Comb (mpg)": fuel_consumption_combG,
    "Transmission": transmission,
    "Fuel Type": fuel_type
}

output = process_car_input(user_input)
output = [output]
print(output)


# check for the position of transmission type that is entered
# same with fuel type

if st.button("Predict"):
    result = classifier.predict(output)
    st.success('The output is {}'.format(result))

