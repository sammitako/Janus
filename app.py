# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
import requests
import googlemaps
import json
import pandas as pd

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	return 'Hello World'

# Helper function to generate a range with floating-point step
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def create_arrests_per_zone_dict():
    # Brendaon
    df = pd.read_csv("NYPD_Arrest_Data__Year_to_Date__20231203.csv", 
                    parse_dates = True, 
                    infer_datetime_format = True, 
                    low_memory=False)
    filtered_df = df[['ARREST_DATE', 'PD_DESC', 'OFNS_DESC', 'LAW_CAT_CD', 'ARREST_BORO', 'AGE_GROUP', 'PERP_SEX', 'PERP_RACE', 'Latitude', 'Longitude']]
    clean_filter = (filtered_df.Latitude > 40) & (filtered_df.Latitude < 41) & (filtered_df.Longitude < -72) & (filtered_df.Longitude > -74.5)
    cleandf = filtered_df[clean_filter]
    # Manhattan Arrests
    man_df = cleandf[cleandf['ARREST_BORO'] == 'M']
    # Define the bin edges for latitude and longitude
    # Latitude: 40.7 to 40.9
    # Longitude: -74.05 to -73.9

    # 40.701505	-74.017166
    # 40.872636	-73.911226
    min_latitude, max_latitude = 40.7, 40.9
    min_longitude, max_longitude = -74.05, -73.9

    # Define the grid step (1 mile difference)
    step = 0.001  # Approximately 1 mile in degrees
    lat_bins = [round(lat, 6) for lat in list(frange(min_latitude, max_latitude, step))]
    lon_bins = [round(lon, 6) for lon in list(frange(min_longitude, max_longitude, step))]

    # Create labels for the bins
    lat_labels = [f'lat_{i}' for i in range(len(lat_bins) - 1)]
    lon_labels = [f'lon_{i}' for i in range(len(lon_bins) - 1)]

    # Bin the latitude and longitude columns
    man_df['lat_bin'] = pd.cut(man_df['Latitude'], bins=lat_bins, labels=lat_labels, include_lowest=True)
    man_df['lon_bin'] = pd.cut(man_df['Longitude'], bins=lon_bins, labels=lon_labels, include_lowest=True)

    # Combine the labels into a single column
    man_df['lat_lon_bin'] = man_df['lat_bin'].astype(str) + '_' + man_df['lon_bin'].astype(str)
    arrests_per_zone_dict = man_df['lat_lon_bin'].value_counts().to_dict()
    return arrests_per_zone_dict

# Function to create a grid
def create_grid():
    # Define the range of coordinates for New York City
    min_latitude, max_latitude = 40.7, 40.9
    min_longitude, max_longitude = -74.05, -73.9
    
    # Define the grid step (1 mile difference)
    step = 0.001  # Approximately 1 mile in degrees
    
    # Create lists of coordinates
    latitudes = [round(lat, 6) for lat in list(frange(min_latitude, max_latitude, step))]
    longitudes = [round(lon, 6) for lon in list(frange(min_longitude, max_longitude, step))]
    
    # Create a list to store grid data
    grid_data = []

    # Populate the list with grid coordinates
    for i in range(len(latitudes) - 1):
        for j in range(len(longitudes) - 1):
            x1, x2 = longitudes[j], longitudes[j + 1]
            y1, y2 = latitudes[i], latitudes[i + 1]
            zone_id = f'lat_{i}_lon_{j}'
            
            grid_data.append({
                'x1-coordinate': x1,
                'y1-coordinate': y1,
                'x2-coordinate': x2,
                'y2-coordinate': y2,
                'zone-id': zone_id
            })
    
    # Create a DataFrame from the list
    df = pd.DataFrame(grid_data)
    
    return df
# lat_199_lon_144


# Create the grid
grid_df = create_grid()
# print(grid_df)
arrests_per_zone_dict = create_arrests_per_zone_dict()
# print(arrests_per_zone_dict)

api_key = "AIzaSyDx7Qa2hpuHNUVjSmesZOc32WhcdRHSWTw"

@app.route('/get_routes_coordinates', methods=['GET'])
def get_routes_coordinates():
    # Get source and destination addresses from the request parameters
    source_address = request.args.get('source_address')
    destination_address = request.args.get('destination_address')

    all_routes_data = get_all_routes_with_coordinates(api_key, source_address, destination_address)
    return identify_routes_risk_score(all_routes_data)

    return all_routes_data


def identify_routes_risk_score(all_routes_data):
    route_object = all_routes_data
    # Function to identify the zone for a given coordinate
    def identify_zone(lat, long, grid_df):
        for index, row in grid_df.iterrows():
            if row['x1-coordinate'] <= long <= row['x2-coordinate'] and row['y1-coordinate'] <= lat <= row['y2-coordinate']:
                return row['zone-id']
        return None  # If the coordinate doesn't fall into any zone

    # Function to identify zones for a route
    def identify_zones_for_route(route_coordinates, grid_df):
        route_zones = []
        for coord in route_coordinates:
            zone = identify_zone(coord['lat'], coord['long'], grid_df)
            route_zones.append(zone)
        return route_zones

    route_zones_data = {}
    # Iterate through each route in the object
    for route_id, route_data in route_object.items():
        route_coordinates = route_data.get("route_coordinates", [])
        
        # Identify zones for the route coordinates
        route_zones = identify_zones_for_route(route_coordinates, grid_df)
        
        # Display the result
        # print(f"Route {route_id}:")
        risk_count = 0
        for coord, zone in zip(route_coordinates, route_zones):
            risk_count += arrests_per_zone_dict[zone]
            # print(f"  Coordinate: {coord}, Zone: {zone}", arrests_per_zone_dict[zone])
        t = {
            "Coordinate": route_coordinates,
            "distance": route_data.get("distance"),
            "time": route_data.get("time"),
            "risk_score": risk_count
        }
        route_zones_data[route_id] = t
        print(route_zones_data)
    return route_zones_data

        # print()



def get_all_routes_with_coordinates(api_key, origin, destination):
    # Initialize the Google Maps API client
    gmaps = googlemaps.Client(key=api_key)

    # Make the directions API request
    directions_result = gmaps.directions(origin, destination, mode="walking", alternatives=True)

    # Extract and format information about each route
    all_routes_data = {}
    for i, route in enumerate(directions_result):
        route_data = {
            "distance": route['legs'][0]['distance']['text'],
            "time": route['legs'][0]['duration']['text'],
            "route_coordinates": []
        }
        count = 0
        for step in route['legs'][0]['steps']:
            if count == 0:
                start_location = step['start_location']
                route_data["route_coordinates"].append({
                    "lat": start_location['lat'],
                    "long": start_location['lng']
                })
                count += 1
            end_location = step['end_location']
            route_data["route_coordinates"].append({
                "lat": end_location['lat'],
                "long": end_location['lng']
            })

        all_routes_data[str(i)] = route_data

    return all_routes_data


# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application 
	# on the local development server.
	app.run()
