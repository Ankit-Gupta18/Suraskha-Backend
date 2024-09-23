import math
import pandas as pd
from sklearn.neighbors import BallTree
import numpy as np
from db.dbmanager import DBManager

# Initialize the database manager
db_manager = DBManager().get_instance()

# Fetch location ratings from the database
location_rating_table = db_manager.fetch_location_ratings()

# Location Rating Schema:
# | id   | latitude  | longitude  | Frequency | Rating |
# |------|-----------|------------|-----------|--------|
# | 1    | 12.993    | 77.543     | 10        | 4      |
# | 2    | 12.9925   | 77.5435    | 5         | 3      |
# | 3    | 12.9935   | 77.542     | 15        | -2     |

# Haversine function to calculate distance between two points (in meters)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in meters

# Function to interpolate points between two route locations (lat/lng)
def interpolate_points(start, end, distance_step=100):
    lat1, lon1 = start['lat'], start['lng']
    lat2, lon2 = end['lat'], end['lng']
    
    total_distance = haversine(lat1, lon1, lat2, lon2)
    
    if total_distance < distance_step:
        return [{'lat': lat1, 'lng': lon1}]
    
    num_steps = int(total_distance // distance_step)
    points = []
    
    for i in range(num_steps + 1):
        fraction = i / num_steps
        lat = lat1 + (lat2 - lat1) * fraction
        lon = lon1 + (lon2 - lon1) * fraction
        points.append({'lat': lat, 'lng': lon})
    
    return points

# Fetch location ratings from database and build a BallTree for efficient querying
def fetch_and_build_tree():
    coordinates = location_rating_table[['latitude', 'longitude']].values
    tree = BallTree(np.radians(coordinates), metric='haversine')  # Use radians for BallTree
    return tree

# Function to calculate the safety index for a route based on location ratings
def calculate_safety_index(route, tree):
    ratings = []
    radius = 300 / 6371000  # 300 meters in radians for the BallTree
    
    for leg in route['legs']:
        for step in leg['steps']:
            start = step['start_location']
            end = step['end_location']
            points = interpolate_points(start, end)

            for point in points:
                point_rad = np.radians([point['lat'], point['lng']])
                distances, indices = tree.query_radius([point_rad], r=radius, return_distance=True)
                
                # For each nearby location rating, apply weight based on distance, frequency, and rating
                for dist, idx in zip(distances[0], indices[0]):
                    rating_row = location_rating_table.iloc[idx]
                    crime_rating = rating_row['Rating']
                    frequency = rating_row['Frequency']
                    weight = (crime_rating * frequency) / ((dist * 6371000) ** 2 + 1)  # Weighted by distance and frequency
                    ratings.append(weight)
    
    if ratings:
        total_weight = sum(ratings)
        safety_index = 1 / (1 + total_weight)  # Inverse of total weighted rating
        return safety_index
    return 1  # Perfect safety if no ratings nearby

# Define routes and calculate safety index for each route
routes = [
    {
        "legs": [
            {
                "steps": [
                    {"start_location": {"lat": 12.99312, "lng": 77.54332}, "end_location": {"lat": 12.99307, "lng": 77.54311}, "distance": 24},
                    {"start_location": {"lat": 12.99307, "lng": 77.54311}, "end_location": {"lat": 12.99316, "lng": 77.54223}, "distance": 94}
                ]
            }
        ]
    }
]

# Fetch location ratings from the database and build BallTree
tree = fetch_and_build_tree()

# Calculate safety index for all routes
for route in routes:
    safety_index = calculate_safety_index(route, tree)
    print(f"Safety Index for Route: {safety_index:.2f}")
