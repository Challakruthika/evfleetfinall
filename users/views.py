from django.shortcuts import render
import pandas as pd
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login as auth_login

def home_view(request):
    return render(request,'users/home_page.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging line
            user = form.save()
            print("User saved to database:", user)  # Debugging line
            return redirect('success_url')
        else:
            print(form.errors)  # This will show form errors in the terminal
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def success_view(request):
    return render(request, 'users/success.html')  # Create a success.html template

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)  # Log the user in
                # Redirect based on user role
                if user.role == 'fleet_manager':
                    return redirect('fleet_manager_home')  # Replace with your fleet manager page
                elif user.role == 'driver':
                    return redirect('driver_home')  # Replace with your driver page
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

def fleet_manager_home_view(request):
    # Logic for the fleet manager's home page
    return render(request, 'users/fleet_manager_home.html')

def driver_home_view(request):
    # Logic for the driver's home page
    return render(request, 'users/driver_home.html')

from django.shortcuts import render

def introduction_to_ev(request):
    return render(request, 'users/introduction_to_ev.html')

def dataset(request):
    return render(request, 'users/dataset.html')

def distribution(request):
    return render(request, 'users/distribution.html')

def relationship(request):
    return render(request, 'users/relationship.html')

def vehicle_status(request):
    return render(request, 'users/vehicle_status.html')

def prediction_view(request):
    return render(request, 'users/prediction.html')  # Adjust as needed

import pandas as pd
from django.shortcuts import render

def vehicle_status(request):
    # Load the dataset with the new path and column name
    df = pd.read_csv('Datasets/EV_Synthetic_Data.csv')  # Adjust the path to your new CSV file
    
    # Check if 'vehicle_status' column exists
    if 'vehicle_status' not in df.columns:
        return render(request, 'users/vehicle_status.html', {'error': "'vehicle_status' column not found in the dataset."})

    # Count the occurrences of each vehicle status
    status_counts = df['vehicle_status'].value_counts()

    # Prepare the data for the bar chart
    data = {
        'labels': ['Inactive', 'Active'],  # Assume 0 -> 'Inactive' and 1 -> 'Active'
        'values': [status_counts.get(0, 0), status_counts.get(1, 0)]  # Default to 0 if not found
    }

    # Pass the data to the template
    return render(request, 'users/vehicle_status.html', {'data': data})

from django.shortcuts import redirect
def relationship_view(request):
    # Replace with the correct address for Streamlit
    return redirect("http://127.0.0.1:8501/")


import pickle
import numpy as np
from django.shortcuts import render
from sklearn.preprocessing import OneHotEncoder

# Load the pre-trained model
with open('users/models/linear_model1.pkl', 'rb') as file:
    model = pickle.load(file)

# Define categories for one-hot encoding (replace with actual categories you used)
make_categories = ['Tesla1', 'Tesla2', 'BMW', 'Polestar', 'Volkswagen']

# Create a helper function for one-hot encoding
def encode_make(make_input):
    return [1 if category == make_input else 0 for category in make_categories[1:]]

# Define the view that will handle the prediction
def predict_range(request):
    # Check if the form is submitted
    if request.method == "POST":
        make_input = request.POST.get('make')  # Get the input vehicle make
        battery_level_input = float(request.POST.get('battery_level'))  # Get the input battery level

        # One-hot encode the 'make' input
        make_one_hot = encode_make(make_input)

        # Prepare the input for prediction (make_one_hot + battery_level)
        input_data = np.array(make_one_hot + [battery_level_input]).reshape(1, -1)

        # Make prediction using the loaded model
        predicted_range = model.predict(input_data)

        # Display the predicted range
        return render(request, 'users/predict_range.html', {
            'predicted_range': predicted_range[0],  # Display the predicted range in the template
        })

    return render(request, 'users/predict_range.html')


# Load the pre-trained model
with open('users/models/linear_model1.pkl', 'rb') as file:
    model = pickle.load(file)

# Define categories for one-hot encoding (replace with actual categories you used)
make_categories = ['Tesla1', 'Tesla2', 'BMW', 'Polestar', 'Volkswagen']

# Create a helper function for one-hot encoding
def encode_make(make_input):
    return [1 if category == make_input else 0 for category in make_categories[1:]]

# Define the view that will handle the prediction
def predict_electric_range(request):
    # Check if the form is submitted
    if request.method == "POST":
        make_input = request.POST.get('make')  # Get the input vehicle make
        battery_level_input = float(request.POST.get('battery_level'))  # Get the input battery level

        # One-hot encode the 'make' input
        make_one_hot = encode_make(make_input)

        # Prepare the input for prediction (make_one_hot + battery_level)
        input_data = np.array(make_one_hot + [battery_level_input]).reshape(1, -1)

        # Make prediction using the loaded model
        predicted_range = model.predict(input_data)

        # Display the predicted range
        return render(request, 'users/prediction.html', {
            'predicted_range': predicted_range[0],  # Display the predicted range in the template
        })

    return render(request, 'users/prediction.html')


from django.shortcuts import render
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from sklearn.preprocessing import MinMaxScaler

# Load dataset
DATA_PATH = "Datasets/EV_Synthetic_Data.csv"
data = pd.read_csv(DATA_PATH)

# Relevant columns for analysis
columns_to_display = [
    "Acceleration 0 - 100 km/h", 
    "Top Speed", 
    "Electric Range", 
    "Total Power", 
    "Total Torque", 
    "Wheelbase", 
    "Gross Vehicle Weight (GVWR)", 
    "Cargo Volume", 
    "Battery Capacity", 
    "Maintenance Cost", 
    "Battery Level", 
    "Range",
    "Make"
]

def relationship_analysis(request):
    x_axis = request.GET.get("x_axis", "Select X")
    y_axis = request.GET.get("y_axis", "Select Y")
    chart_type = request.GET.get("chart_type", "Bar Chart")
    plot_div = None

    if x_axis != "Select X" and y_axis != "Select Y" and x_axis in data.columns and y_axis in data.columns:
        # Clean data and scale selected columns
        data_clean = data.dropna(subset=[x_axis, y_axis])
        scaler = MinMaxScaler()
        data_clean[x_axis] = scaler.fit_transform(data_clean[[x_axis]])
        data_clean[y_axis] = scaler.fit_transform(data_clean[[y_axis]])

        # Generate chart based on the selected type
        if chart_type == "Bar Chart":
            fig = px.bar(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
        elif chart_type == "Scatter Plot":
            fig = px.scatter(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
        elif chart_type == "Line Chart":
            fig = px.line(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
        elif chart_type == "Area Chart":
            fig = px.area(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
        elif chart_type == "Pie Chart":
            if x_axis == "Make":  # Pie chart works with categorical data
                fig = px.pie(data_clean, names="Make", title=f"{chart_type} of Vehicle Make")
            else:
                fig = px.pie(data_clean, values=y_axis, names=x_axis, title=f"{chart_type}: {x_axis} vs {y_axis}")

        # Convert Plotly figure to HTML div
        plot_div = plot(fig, output_type="div")

    return render(request, "users/relationship_analysis.html", {
        "columns": columns_to_display,
        "plot_div": plot_div,
        "selected_x": x_axis,
        "selected_y": y_axis,
        "selected_chart": chart_type
    })


from django.contrib.auth import logout
def custom_logout_view(request):
    """Logs out the user and redirects to the homepage."""
    logout(request)  # Logs out the user
    return redirect("home")