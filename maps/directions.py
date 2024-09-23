import os
import json
from py_olamaps.OlaMaps import OlaMaps

def get_routing_directions(start_lat, start_lon, end_lat, end_lon):
    # Initialize the OlaMaps client with the API key
    client = OlaMaps(
        api_key="SPFxc71FNc3LIdEcqyfDsg01EhUM41Nkq43BiRQf"
    )
    
    # Format the start and end coordinates
    start_location = f"{start_lat},{start_lon}"
    end_location = f"{end_lat},{end_lon}"
    
    # Fetch routing directions
    routing_direction = client.routing.directions(
        start_location,
        end_location,
        alternatives=True
    )
    
    return routing_direction

# # Example usage
# start_latitude = 12.993103152916301
# start_longitude = 77.54332622119354
# end_latitude = 12.972006793201695
# end_longitude = 77.5800850011884

# directions = get_routing_directions(start_latitude, start_longitude, end_latitude, end_longitude)
# print(json.dumps(directions, indent=2))

# # Save the response into a JSON file
# file_path = "routing_direction.json"  # File name to save the response

# # Write the response to a JSON file
# with open(file_path, "w") as json_file:
#     json.dump(routing_direction, json_file, indent=4)

# print(f"Routing direction saved to {file_path}")
