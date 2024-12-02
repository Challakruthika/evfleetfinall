#SYNTHETIC DATA GENERATION
#pip install faker
import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Vehicle specs from the image
vehicle_specs = {
    "Tesla1": {"Acceleration": 4.4, "Top Speed": 233, "Electric Range": 485, "Total Power": 366, "Total Torque": 493, "Drive": "AWD", "Battery Capacity": 82, "Length": 4694, "Width": 1849, "Height": 1443, "Wheelbase": 2875, "Gross Vehicle Weight": 2232, "Max Payload": 388, "Cargo Volume": 561, "Seats": 5},
    "Tesla2": {"Acceleration": 3.3, "Top Speed": 261, "Electric Range": 460, "Total Power": 377, "Total Torque": 660, "Drive": "AWD", "Battery Capacity": 82, "Length": 4694, "Width": 1849, "Height": 1443, "Wheelbase": 2875, "Gross Vehicle Weight": 2232, "Max Payload": 388, "Cargo Volume": 561, "Seats": 5},
    "BMW": {"Acceleration": 5.7, "Top Speed": 190, "Electric Range": 470, "Total Power": 250, "Total Torque": 430, "Drive": "Rear", "Battery Capacity": 83.9, "Length": 4783, "Width": 1852, "Height": 1448, "Wheelbase": 2856, "Gross Vehicle Weight": 2605, "Max Payload": 555, "Cargo Volume": 470, "Seats": 5},
    "Volkswagen": {"Acceleration": 7.9, "Top Speed": 160, "Electric Range": 450, "Total Power": 150, "Total Torque": 310, "Drive": "Rear", "Battery Capacity": 82, "Length": 4261, "Width": 1809, "Height": 1568, "Wheelbase": 2771, "Gross Vehicle Weight": 2300, "Max Payload": 447, "Cargo Volume": 385, "Seats": 5},
    "Polestar": {"Acceleration": 7.4, "Top Speed": 160, "Electric Range": 425, "Total Power": 170, "Total Torque": 330, "Drive": "Front", "Battery Capacity": 78, "Length": 4607, "Width": 1800, "Height": 1479, "Wheelbase": 2735, "Gross Vehicle Weight": 2490, "Max Payload": 496, "Cargo Volume": 405, "Seats": 5},
}

# Initialize data lists
data = []
roles = ["Driver"] * 1600 + ["Fleet Manager"] * 400  # 1600 drivers, 400 fleet managers
random.shuffle(roles)  # Shuffle roles to randomize

# Generate 2000 records
for i in range(1, 2001):
    # Synthetic username and email
    username = fake.user_name()
    email = f"{username}@gmail.com"

    # Role (Driver or Fleet Manager)
    role = roles[i - 1]

    # Random vehicle make
    make = random.choice(list(vehicle_specs.keys()))
    specs = vehicle_specs[make]

    # Maintenance cost and pincode
    maintenance_cost = round(random.uniform(1000, 5000), 2)  # Random maintenance cost
    pincode = fake.postcode()

    # Date, time, location
    date = fake.date_this_year()
    time = fake.time()
    latitude = round(random.uniform(-90.0, 90.0), 6)
    longitude = round(random.uniform(-180.0, 180.0), 6)

    # Vehicle status
    vehicle_status = random.choice([0, 1])

    # Battery level and range
    battery_level = random.randint(1, 100)
    range_per_percent = specs["Electric Range"] / 100
    range_km = round(battery_level * range_per_percent, 2)

    # Append record
    data.append({
        "id": i,
        "username": username,
        "email": email,
        "role": role,
        "make": make,
        "acceleration": specs["Acceleration"],
        "top_speed": specs["Top Speed"],
        "electric_range": specs["Electric Range"],
        "total_power": specs["Total Power"],
        "total_torque": specs["Total Torque"],
        "drive": specs["Drive"],
        "battery_capacity": specs["Battery Capacity"],
        "length": specs["Length"],
        "width": specs["Width"],
        "height": specs["Height"],
        "wheelbase": specs["Wheelbase"],
        "gross_vehicle_weight": specs["Gross Vehicle Weight"],
        "max_payload": specs["Max Payload"],
        "cargo_volume": specs["Cargo Volume"],
        "seats": specs["Seats"],
        "maintenance_cost": maintenance_cost,
        "pincode": pincode,
        "date": date,
        "time": time,
        "latitude": latitude,
        "longitude": longitude,
        "vehicle_status": vehicle_status,
        "battery_level": battery_level,
        "range": range_km
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('EV_Synthetic_Data_New.csv', index=False)

print("Synthetic dataset created and saved as 'EV_Synthetic_Data_New.csv'.")


import pandas as pd

# Load the dataset
df = pd.read_csv("/content/EV_Synthetic_Data_New.csv")

# Count the occurrences of each role
role_counts = df['role'].value_counts()

# Display the counts
print("Role Counts:")
print(role_counts)

# For specific counts
drivers_count = role_counts.get('Driver', 0)
fleet_managers_count = role_counts.get('Fleet Manager', 0)

print(f"\nDrivers: {drivers_count}")
print(f"Fleet Managers: {fleet_managers_count}")


# Count the occurrences of each make
make_counts = df['make'].value_counts()

# Display the counts
print("Vehicle Counts by Make:")
print(make_counts)

# For specific counts (if needed)
tesla1_count = make_counts.get('Tesla1', 0)
tesla2_count = make_counts.get('Tesla2', 0)
bmw_count = make_counts.get('BMW', 0)
volkswagen_count = make_counts.get('Volkswagen', 0)
polestar_count = make_counts.get('Polestar', 0)

print(f"\nTesla1: {tesla1_count}")
print(f"Tesla2: {tesla2_count}")
print(f"BMW: {bmw_count}")
print(f"Volkswagen: {volkswagen_count}")
print(f"Polestar: {polestar_count}")



#MODELING PART-LINEAR REGRESSION MODEL
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

# Load dataset
df = pd.read_csv("/content/EV_Synthetic_Data_New.csv")

# Introduce noise to the target variable (range)
np.random.seed(42)
noise = np.random.normal(loc=0, scale=42, size=df.shape[0])  # Adjust scale for desired R²
df['range_noisy'] = df['range'] + noise

# Extract features and target
X = df[['make', 'battery_level']]  # Features: make and battery_level
y = df['range_noisy']  # Target: range with noise

# One-Hot Encoding for 'make'
encoder = OneHotEncoder(sparse_output=False,drop="first")  # Use sparse_output=False
make_encoded = encoder.fit_transform(X[['make']])

# Combine the encoded 'make' with 'battery_level'
X_preprocessed = np.hstack([make_encoded, X[['battery_level']].values])

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Calculate MSE and R² score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")

# Example: User inputs
user_make = "Tesla2"  # Example make
user_battery_level = 74  # Example battery level

# Encode the 'make' input
user_make_encoded = encoder.transform([[user_make]])

# Combine encoded 'make' with battery level
user_input = np.hstack([user_make_encoded, [[user_battery_level]]])

# Predict the range
predicted_range = model.predict(user_input)[0]
print(f"Predicted Range for {user_make} at {user_battery_level}% battery level: {predicted_range} km")


#ENCODER PICKLE FILE CREATION
import pickle
from sklearn.preprocessing import OneHotEncoder

# Assuming 'encoder' is your fitted OneHotEncoder
encoder = OneHotEncoder(sparse_output=False)  # Example encoder

# After fitting the encoder with your training data
encoder.fit(X[['make']])  # X is your input dataframe with 'make' column

# Save the encoder to a file
with open('encoder.pkl', 'wb') as file:
    pickle.dump(encoder, file)

print("Encoder saved!")



#TESTING
import numpy as np

# Define the input values
make_input = 'BMW'          # Make of the vehicle
battery_level_input = 83   # Battery level

# One-hot encode the 'make' input
# Ensure the order of categories matches the encoder's fit during training
make_categories = encoder.categories_[0]  # Retrieve categories learned by the encoder
make_one_hot = [1 if category == make_input else 0 for category in make_categories[1:]]  # Skip the first category (dropped)

# Combine the encoded 'make' and 'battery_level' into the input array
input_data = np.array(make_one_hot + [battery_level_input]).reshape(1, -1)

# Predict the range
predicted_range = model.predict(input_data)

# Output the prediction
print(f"Predicted range for make '{make_input}' with battery level {battery_level_input}%: {predicted_range[0]:.2f} km")




#ELASTIC NET REGRESSION
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, r2_score

# Train Elastic Net Regression model
elastic_net_model = ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42)
elastic_net_model.fit(X_train, y_train)  # Train using preprocessed data

# Predict on the test data
y_pred_elastic_net = elastic_net_model.predict(X_test)

# Calculate R² score and MSE
r2_elastic_net = r2_score(y_test, y_pred_elastic_net)
mse_elastic_net = mean_squared_error(y_test, y_pred_elastic_net)

# Print the metrics
print(f"Elastic Net Regression:")
print(f"R² Score: {r2_elastic_net:.2f}")
print(f"Mean Squared Error (MSE): {mse_elastic_net:.2f}")

# Predict the range for a specific input
make_one_hot = [1 if category == make_input else 0 for category in make_categories[1:]]  # Skip the first category
input_data = np.array(make_one_hot + [battery_level_input]).reshape(1, -1)
predicted_range_elastic_net = elastic_net_model.predict(input_data)

print(f"Predicted range using Elastic Net for make '{make_input}' with battery level {battery_level_input}%: {predicted_range_elastic_net[0]:.2f} km")



#RIDGE REGRESSION
from sklearn.linear_model import Ridge

# Train Ridge Regression model
ridge_model = Ridge(alpha=1.0, random_state=42)
ridge_model.fit(X_train, y_train)  # Train using preprocessed data

# Predict on the test data
y_pred_ridge = ridge_model.predict(X_test)

# Calculate R² score and MSE
r2_ridge = r2_score(y_test, y_pred_ridge)
mse_ridge = mean_squared_error(y_test, y_pred_ridge)

# Print the metrics
print(f"\nRidge Regression:")
print(f"R² Score: {r2_ridge:.2f}")
print(f"Mean Squared Error (MSE): {mse_ridge:.2f}")

# Predict the range for a specific input
predicted_range_ridge = ridge_model.predict(input_data)

print(f"Predicted range using Ridge Regression for make '{make_input}' with battery level {battery_level_input}%: {predicted_range_ridge[0]:.2f} km")


#CONVERTING TO PICKLE
import pickle
from sklearn.linear_model import LinearRegression

# Assuming you have already trained your model (linear_model) as shown in the previous steps
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Save the model to a pickle file
with open('linear_model1.pkl', 'wb') as file:
    pickle.dump(linear_model, file)

print("Linear Regression model saved as pickle file.")
