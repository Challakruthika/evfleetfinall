import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_csv("Datasets/EV_Synthetic_Data.csv")

# List of columns to be used in the dropdown
columns_to_display = [
    "acceleration", 
    "top_speed", 
    "electric_range", 
    "total_power", 
    "total_torque", 
    "wheelbase", 
    "gross_vehicle_weight", 
    "cargo_volume", 
    "battery_capacity", 
    "maintenance_cost", 
    "battery_level", 
    "range",
    "make"
]

# Streamlit Sidebar for feature selection
st.sidebar.header("Explore Relationships Between Features")
feature_1 = st.sidebar.selectbox("Choose the first feature to explore:", options=["Choose a feature"] + columns_to_display)
feature_2 = st.sidebar.selectbox("Choose the second feature to explore:", options=["Choose a feature"] + columns_to_display)

# Ensure selected columns are numeric for plotting
if feature_1 != "Choose a feature" and feature_2 != "Choose a feature":  # Make sure user selects valid features
    # Clean the data: Drop rows with missing values for the selected features
    data_clean = data.dropna(subset=[feature_1, feature_2])

    # Normalize data if necessary (example: Min-Max scaling for the selected columns)
    scaler = MinMaxScaler()
    data_clean[feature_1] = scaler.fit_transform(data_clean[[feature_1]])
    data_clean[feature_2] = scaler.fit_transform(data_clean[[feature_2]])

    # Create Bar Chart
    bar_fig = px.bar(data_clean, x=feature_1, y=feature_2, title=f"{feature_1.replace('_', ' ').title()} vs {feature_2.replace('_', ' ').title()} (Bar Chart)", color="make")

    # Create Histogram for the first feature
    hist_fig = px.histogram(data_clean, x=feature_1, title=f"Distribution of {feature_1.replace('_', ' ').title()}")

    # Create Box Plot for the second feature
    box_fig = px.box(data_clean, y=feature_2, title=f"Distribution of {feature_2.replace('_', ' ').title()}")

    # Create Pie Chart based on "make" column
    pie_fig = px.pie(data, names='make', title="Vehicle Distribution by Make")

    # Create Area Chart
    area_fig = px.area(data_clean, x=feature_1, y=feature_2, title=f"{feature_1.replace('_', ' ').title()} vs {feature_2.replace('_', ' ').title()} (Area Chart)", color="make")

    # Display the charts
    st.title("Vehicle Data Insights")

    # Display Bar Chart
    st.plotly_chart(bar_fig, use_container_width=True)

    # Display Histogram
    st.plotly_chart(hist_fig, use_container_width=True)

    # Display Box Plot
    st.plotly_chart(box_fig, use_container_width=True)

    # Display Pie Chart
    st.plotly_chart(pie_fig, use_container_width=True)

    # Display Area Chart
    st.plotly_chart(area_fig, use_container_width=True)

else:
    st.info("Select two features to compare and explore the insights.")
