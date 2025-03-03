import streamlit as st
import pickle
import pandas as pd
from scipy.stats import percentileofscore
from PIL import Image


# Load the model
pickle_in = open('best_model_MLP_subset1.pkl', 'rb')
classifier = pickle.load(pickle_in)

@st.cache_data
def load_data():
    file_path = "2025cardata.xlsx"  # Ensure this is the correct path
    xls = pd.ExcelFile(file_path, engine="openpyxl")
    df_2025 = pd.read_excel(xls, sheet_name="2025")
    return df_2025

df = load_data()

df['City CO2 Percentile'] = df['City CO2 Rounded Adjusted'].apply(lambda x: percentileofscore(df['City CO2 Rounded Adjusted'], x))
df['Hwy CO2 Percentile'] = df['Hwy CO2 Rounded Adjusted'].apply(lambda x: percentileofscore(df['Hwy CO2 Rounded Adjusted'], x))
df['Comb CO2 Percentile'] = df['Comb CO2 Rounded Adjusted (as shown on FE Label)'].apply(lambda x: percentileofscore(df['Comb CO2 Rounded Adjusted (as shown on FE Label)'], x))

def get_color(percentile):
    if percentile <= 25:
        return "green"
    elif percentile <= 50:
        return "yellowgreen"
    elif percentile <= 75:
        return "orange"
    else:
        return "red"
    
def display_emission_data(label, value, percentile):
    bar_color = get_color(percentile)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <div style="width: 200px; background-color: lightgray; border-radius: 5px; overflow: hidden;">
                <div style="width: {percentile}%; background-color: {bar_color}; padding: 5px; text-align: right; color: white; font-weight: bold;">
                    {int(percentile)}%
                </div>
            </div>
            <div style="margin-left: 10px;"><strong>{label}:</strong> {value} g/mile</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def emission_search():
    st.title("Search CO2 Emission Ratings")

    st.write("In contrast to the previous page, this search engine is not run with Artifical Intelligence. Instead, it directly takes data from a large database provided by the United States Environemntal Protection Agency (EPA).")

    st.write("In this page, you can simply enter a vehicle brand and model and you will recieve a percentile rating of how much carbon dioxide is emitted by the vehicle. The lower the percentile, the better for the environment!")

    st.write("You can use this page to make a greener decision on what vehicle model you would like to buy. For example, if you know you want an Audi but you don't care much about the model, you could use this tool to pick the Audi model with the least percentile rating!")

    st.write("**This page is designed as a supplement to the last, as it doesn't focus on car settings and rather helps you with the first decision: buying the vehicle.**")
    st.write("-------------------------------")
    
    # Select a car brand
    brands = df['Division'].unique()
    selected_brand = st.selectbox("Select Brand", brands)
    
    # Filter car models based on brand
    car_models = df[df['Division'] == selected_brand]['Carline'].unique()
    selected_model = st.selectbox("Select Model", car_models)
    
    # Retrieve and display emission data
    filtered_df = df[(df['Division'] == selected_brand) & (df['Carline'] == selected_model)]
    
    if not filtered_df.empty:
        st.write("### CO2 Emission Ratings")
        
        city_co2 = filtered_df['City CO2 Rounded Adjusted'].values[0]
        hwy_co2 = filtered_df['Hwy CO2 Rounded Adjusted'].values[0]
        comb_co2 = filtered_df['Comb CO2 Rounded Adjusted (as shown on FE Label)'].values[0]

        city_percentile = filtered_df['City CO2 Percentile'].values[0]
        hwy_percentile = filtered_df['Hwy CO2 Percentile'].values[0]
        comb_percentile = filtered_df['Comb CO2 Percentile'].values[0]

        # Display Color-Coded Emission Data
        display_emission_data("City CO2 Emissions", city_co2, city_percentile)
        display_emission_data("Highway CO2 Emissions", hwy_co2, hwy_percentile)
        display_emission_data("Combined CO2 Emissions", comb_co2, comb_percentile)

    else:
        st.write("No data available for the selected car.")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Feature Engineering", "Predict", "CO2 Emission by Car Brand"])

if section == "Home":
    st.title("Carbon Emission Trends")
    img_url = "carbonbanner.jpg"
    image = Image.open(img_url)
    st.image(image, caption="Vehicle Pollution")
    st.header("About the Project")
    st.write("One of the biggest contributers to climate change is the emission of greenhouse gas, which has accelerated global warming and caused increased rates of natural disasters like forest fires, which have affected us greatly in the past few years (LA Fires of 2025, Canadian Wildfires of 2023). Surprisingly, transport accounts for around a quarter of global carbon emissions, wherein vehicles supply three quarters (18.75 percent of total).")
    st.write("Therefore, it is up to us as consumers to be aware of how our choices affect the environment. Using my machine learning model with an R2 score of almost 0.996 on unseen test data, you can see just how much of a difference our consumer choices make.")
    st.write("If you want to check out how car brands and models affect emissions, check out the feature engineering tab and use the data to make a smart, environmentally efficient consumer choice for the Earth!")

elif section == "Feature Engineering":
    # About Section
    st.title("Feature Engineering: Key Insights on CO2 Emissions")
    
    # Highlight Factors Related to Emissions
    st.header("Factors Most Related to Carbon Emissions")
    st.write("(Predicted by Our Model, Rounded to Nearest Integer)")
    
    st.markdown("""
    ### 🚀 Top Factors Driving CO2 Emissions:
    1. **Fuel Consumption**:
       - a. City (40% of total importance)
       - b. Combined (21% of total importance)  
       - c. Highway (15% of total importance)
    2. **Fuel Type**:
       - a. Ethanol (15% of total importance, **reduction in CO2**)  
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
    5. **Image**:
    """)
    
    # Add a Visual Element
    st.image("featureimportance.png", caption="Factors influencing CO2 emissions", use_container_width=True)
    
    # Concluding Message
    st.write("**Conclusion:**")
    st.markdown("""
    Understanding these factors helps us identify key areas to target for reducing carbon emissions. 
    The factor that most overwhelmingly leads to CO2 emissions is of course **fuel consumption**, but beyond that, 
    **ethanol** fuel seems to have a very large impact on emissions (12% **REDUCTION IN CO2**). Ethanol is tailed by the other fuel types, 
    which have a lower impact on the total CO2 emissions (2-3%). Suprisingly, cylinders and transmission don't make
    very large impacts, but it is worth noting that **AS8** affects carbon emissions most. Together, we can make driving more eco-friendly!
    """)


elif section == "Predict":
    # Prediction Section
    st.title("Predict YOUR Emissions Using AI!")

    st.write("In this section, you can use my deep learning regression model with an r2 score of 0.996 (99th percentile) to see how car settings affect overall carbon emissions. Testing data from the 'Feature Engineering' tab shows that using **ethanol** as your fuel type will heavily **reduce** emissions and increasing **fuel consumption** will obviously **increase** carbon emissions.")
    
    st.write("Feel free to play around with values, and you can even input your own values from a recent drive!")
    st.write("-------------------------------")

    st.write("Enter your values below: ")
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
        engine_size = st.slider("Engine Size (L)", 0.0, 10.0, 0.1)      #text_input("Engine Size (L)")
        cylinders = st.slider("Number of Cylinders", 4, 12, 1) 
        transmission = st.selectbox("Transmission Type", transmission_options)
        st.write("<small><i>A = Automatic, AM = Automated Manual, AS = Automatic w/ Select Shift, AV = Cotinuously Variable, 3-10 = Number of Gears", unsafe_allow_html=True)
        fuel_consumption_city = st.slider("Fuel Consumption City (L/100 km)", 0.0, 40.0, 0.1)
        fuel_consumption_hwy = st.slider("Fuel Consumption Highway (L/100 km)", 0.0, 40.0, 0.1)
        fuel_consumption_combL = st.slider("Fuel Consumption Combined (L/100 km)", 0.0, 40.0, 0.1)
        fuel_consumption_combG = st.slider("Fuel Consumption Combined (mpg)", 0.0, 80.0, 0.1)

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
                st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #ff5733; font-size: 40px;">Your Fuel Economy is: {result:.2f} g/km</h1>
                </div>
                <div style="background-color: #AFEA2E; padding: 10px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #000000; font-size: 35px;">Classification: {classification} </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
            elif 199 <= result < 230:
                classification = 'Low'
                st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #ff5733; font-size: 40px;">Your Fuel Economy is: {result:.2f} g/km</h1>
                </div>
                <div style="background-color: #C5E42B; padding: 10px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #000000; font-size: 35px;">Classification: {classification} </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
            elif 230 <= result < 260:
                classification = 'Medium'
                st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #ff5733; font-size: 40px;">Your Fuel Economy is: {result:.2f} g/km</h1>
                </div>
                <div style="background-color: #F0F811; padding: 10px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #000000; font-size: 35px;">Classification: {classification} </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
            elif 260 <= result < 298:
                classification = 'High'
                st.markdown(
                f"""
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #ff5733; font-size: 40px;">Your Fuel Economy is: {result:.2f} g/km</h1>
                </div>
                <div style="background-color: ##F86911; padding: 10px; border-radius: 5px; text-align: center;">
                    <h1 style="color: #000000; font-size: 35px;">Classification: {classification} </h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
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
elif section == "CO2 Emission by Car Brand":
    emission_search()