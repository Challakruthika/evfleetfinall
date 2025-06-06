from django.shortcuts import render
import pandas as pd
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
import numpy as np
import pickle
import os
from sklearn.preprocessing import OneHotEncoder
import plotly.express as px
from plotly.offline import plot
from sklearn.preprocessing import MinMaxScaler

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
    try:
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'Datasets', 'EV_Synthetic_Data.csv'))
        
        if 'vehicle_status' not in df.columns:
            return render(request, 'users/vehicle_status.html', 
                        {'error': "'vehicle_status' column not found in the dataset."})

        status_counts = df['vehicle_status'].value_counts()
        data = {
            'labels': ['Inactive', 'Active'],
            'values': [status_counts.get(0, 0), status_counts.get(1, 0)]
        }
        return render(request, 'users/vehicle_status.html', {'data': data})
    except Exception as e:
        return render(request, 'users/vehicle_status.html', 
                    {'error': f"Error loading data: {str(e)}"})

def prediction_view(request):
    return render(request, 'users/prediction.html')  # Adjust as needed

from django.shortcuts import redirect
def relationship_view(request):
    # Replace with the correct address for Streamlit
    return redirect("http://127.0.0.1:8501/")

def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'users', 'models', 'linear_model1.pkl')
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def encode_make(make_input):
    return [1 if category == make_input else 0 for category in make_categories[1:]]

def predict_range(request):
    if request.method == "POST":
        try:
            model = load_model()
            if model is None:
                return render(request, 'users/predict_range.html', 
                            {'error': 'Could not load the prediction model'})

            make_input = request.POST.get('make')
            battery_level_input = float(request.POST.get('battery_level'))
            make_one_hot = encode_make(make_input)
            input_data = np.array(make_one_hot + [battery_level_input]).reshape(1, -1)
            predicted_range = model.predict(input_data)

            return render(request, 'users/predict_range.html', {
                'predicted_range': predicted_range[0],
                'make': make_input,
                'battery_level': battery_level_input
            })
        except Exception as e:
            return render(request, 'users/predict_range.html', 
                        {'error': f'Prediction error: {str(e)}'})

    return render(request, 'users/predict_range.html')

def predict_electric_range(request):
    if request.method == "POST":
        try:
            model = load_model()
            if model is None:
                return render(request, 'users/prediction.html', 
                            {'error': 'Could not load the prediction model'})

            make_input = request.POST.get('make')
            battery_level_input = float(request.POST.get('battery_level'))
            make_one_hot = encode_make(make_input)
            input_data = np.array(make_one_hot + [battery_level_input]).reshape(1, -1)
            predicted_range = model.predict(input_data)

            return render(request, 'users/prediction.html', {
                'predicted_range': predicted_range[0],
                'make': make_input,
                'battery_level': battery_level_input
            })
        except Exception as e:
            return render(request, 'users/prediction.html', 
                        {'error': f'Prediction error: {str(e)}'})

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
    try:
        data = pd.read_csv(os.path.join(settings.BASE_DIR, 'Datasets', 'EV_Synthetic_Data.csv'))
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

        x_axis = request.GET.get("x_axis", "Select X")
        y_axis = request.GET.get("y_axis", "Select Y")
        chart_type = request.GET.get("chart_type", "Bar Chart")
        plot_div = None

        if x_axis != "Select X" and y_axis != "Select Y" and x_axis in data.columns and y_axis in data.columns:
            data_clean = data.dropna(subset=[x_axis, y_axis])
            
            if x_axis != "Make" and y_axis != "Make":
                scaler = MinMaxScaler()
                data_clean[x_axis] = scaler.fit_transform(data_clean[[x_axis]])
                data_clean[y_axis] = scaler.fit_transform(data_clean[[y_axis]])

            if chart_type == "Bar Chart":
                fig = px.bar(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
            elif chart_type == "Scatter Plot":
                fig = px.scatter(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
            elif chart_type == "Line Chart":
                fig = px.line(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
            elif chart_type == "Area Chart":
                fig = px.area(data_clean, x=x_axis, y=y_axis, title=f"{chart_type}: {x_axis} vs {y_axis}", color="Make")
            elif chart_type == "Pie Chart":
                if x_axis == "Make":
                    fig = px.pie(data_clean, names="Make", title=f"{chart_type} of Vehicle Make")
                else:
                    fig = px.pie(data_clean, values=y_axis, names=x_axis, title=f"{chart_type}: {x_axis} vs {y_axis}")

            plot_div = plot(fig, output_type="div")

        return render(request, "users/relationship_analysis.html", {
            "columns": columns_to_display,
            "plot_div": plot_div,
            "selected_x": x_axis,
            "selected_y": y_axis,
            "selected_chart": chart_type
        })
    except Exception as e:
        return render(request, "users/relationship_analysis.html", {
            "columns": columns_to_display,
            "error": f"Error analyzing relationships: {str(e)}"
        })

from django.contrib.auth import logout
def custom_logout_view(request):
    """Logs out the user and redirects to the homepage."""
    logout(request)  # Logs out the user
    return redirect("home")