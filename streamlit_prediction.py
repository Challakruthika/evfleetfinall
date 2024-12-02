import streamlit as st
import pickle
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Load the model from the pickle file
model_path = os.path.join('users', 'models', 'linear_model.pkl')  # Path to the pickle file
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load the OneHotEncoder used during training
encoder = pickle.load(open('users/models/encoder.pkl', 'rb'))  # Make sure the encoder is saved and loaded

# Streamlit UI
st.title('Electric Range Prediction')

# Input fields
make = st.selectbox('Select the Make of the vehicle', ['BMW', 'Polestar', 'Tesla1', 'Tesla2', 'Volkswagen'])
battery_level = st.number_input('Enter Battery Level (in %)', min_value=0, max_value=100, step=1)

# Function to one-hot encode the selected make
def encode_make(make):
    # One-hot encoding based on the training dataset
    make_encoded = encoder.transform([[make]])  # Use the same encoder as during training
    return make_encoded

# Prepare the input for prediction
encoded_make = encode_make(make)
prediction_input = np.hstack([encoded_make, [[battery_level]]])  # Combine encoded 'make' with battery level

# Prediction on button click
if st.button('Predict'):
    try:
        # Make prediction
        predicted_range = model.predict(prediction_input)

        # Display result
        st.write(f'The estimated electric range is: {predicted_range[0]:.2f} km')
    except Exception as e:
        st.error(f"Error: {e}")
