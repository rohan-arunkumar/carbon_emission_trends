import streamlit as st
import pickle
from PIL import Image

# Load the model
pickle_in = open('best_model_MLP_subset1.pkl', 'rb')
classifier = pickle.load(pickle_in)

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Feature Engineering", "Predict"])

if section == "Home":
    st.title("Carbon Emission Trends")
    img_url = "carbonbanner.jpg"
    image = Image.open(img_url)
    st.image(image, caption="Vehicle Pollution")
    st.header("About the Project")
    st.write("One of the biggest contributers to global warming is the emission of greenhouse gas, which have already tore a hole in the Earth's ozone layer, exposing us to harmful radiation and speeding up the climate clock. Surprisingly, transport accounts for around a quarter of global carbon emissions, wherein vehicles supply three quarters (18.75 percent of total).")
    st.write("Therefore, it is up to us as consumers to be aware of how our choices affect the environment. Using my machine learning model with an R2 score of almost 0.99, you can see just how much of a difference our consumer choices make.")
    st.write("If you want to check out how car brands and models affect emissions, check out the feature engineering tab and use the data to make a smart, environmentally efficient consumer choice for the Earth!")

elif section == "Feature Engineering":
    # About Section
    st.title("Feature Engineering: Key Insights on CO2 Emissions")
    
    # Highlight Factors Related to Emissions
    st.header("Factors Most Related to Carbon Emissions")
    st.write("(Predicted by Our Model, Rounded to Nearest Int)")
    
    st.markdown("""
    ### 🚀 Top Factors Driving CO2 Emissions:
    1. **Fuel Consumption**:
       - a. City (40% of total importance)
       - b. Combined (21% of total importance)  
       - c. Highway (15% of total importance)

    2. **Fuel Type**:
       - a. Ethanol (15% of total importance)  
       - b. Regular Gasoline (3% of total importance)  
       - c. Premium Gasoline (3% of total importance)
       - d. Diesel (2% of total importance)  
       
    3. **Cylinders**:
       - a. Number of Cylinders (0.05% importance)

    4. **Transmission**:
       - a. AS8 (0.1% of total importance) 
       - b. M6 (0.09% of total importance)
       - c. AM7 (0.08% of total importance) 
       - d. AS6 (0.05% of total importance)
       - e. A8, A9 (0.04% of total importance)
       - f. AS10, A6, AV, AS7 (0.02% of total importance)
       - g. ALL OTHER TRANSMISSIONS ARE NEGLIGABLE (<0.01% of total importance)
    """)
    
    # Add a Visual Element
    st.image("path_to_relevant_image.jpg", caption="Factors influencing CO2 emissions", use_container_width=True)
    
    # Concluding Message
    st.markdown("""
    Understanding these factors helps us identify key areas to target for reducing carbon emissions. Together, we can make driving more eco-friendly! 🌍
    """)


elif section == "Predict":
    # Prediction Section
    st.title("Predict Using AI")

    # Using a form to group inputs
    with st.form(key="prediction_form"):
        fuel_type_options = ['D', 'E', 'X', 'Z']
        transmission_options = [
            'A10', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AM5', 'AM6',
            'AM7', 'AM8', 'AM9', 'AS10', 'AS4', 'AS5', 'AS6', 'AS7', 'AS8',
            'AS9', 'AV', 'AV10', 'AV6', 'AV7', 'AV8', 'M5', 'M6', 'M7'
        ]
        fuel_type = st.selectbox("Fuel Type", fuel_type_options)
        st.write("<small><i>D = Diesel, E = Ethanol, X = Regular Gasoline, Z = Premium Gasoline", unsafe_allow_html=True)
        engine_size = st.text_input("Engine Size (L)")
        cylinders = st.text_input("Number of Cylinders")
        transmission = st.selectbox("Transmission Type", transmission_options)
        st.write("<small><i>A = Automatic, AM = Automated Manual, AS = Automatic w/ Select Shift, AV = Cotinuously Variable, 3-10 = Number of Gears", unsafe_allow_html=True)
        fuel_consumption_city = st.text_input("Fuel Consumption City (L/100 km)")
        fuel_consumption_hwy = st.text_input("Fuel Consumption Highway (L/100 km)")
        fuel_consumption_combL = st.text_input("Fuel Consumption Combined (L/100 km)")
        fuel_consumption_combG = st.text_input("Fuel Consumption Combined (mpg)")

        # Submit button for the form
        submit_button = st.form_submit_button(label="Predict")

    if submit_button:
        # Check for missing inputs
        if not all([fuel_type, engine_size, cylinders, transmission, fuel_consumption_city, fuel_consumption_hwy, fuel_consumption_combL, fuel_consumption_combG]):
            st.error("Please fill in all fields before making a prediction.")
        else:
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
                output_list = list(map(float, output_list))
                return [output_list]

            # Process the user input
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
            result = classifier.predict(output)
            result = result[0]
            if result < 199:
                classification = 'Very Low'
            elif 199 <= result < 230:
                classification = 'Low'
            elif 230 <= result < 260:
                classification = 'Medium'
            elif 260 <= result < 298:
                classification = 'High'
            else:
                classification = 'Very High'
            st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #ff5733; font-size: 40px;">Your Fuel Economy is: {result:.2f} g/km</h1>
                </div>
                <div style="background-color: #ff5733; padding: 10px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #000000; font-size: 35px;">Classification: {classification} </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # st.write(f'The amount of CO2 (g/km) released into the air is:')
            # st.subheader(result)