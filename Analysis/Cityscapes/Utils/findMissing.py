import json

def load_trafficsigns_list_from_json(file_path):
    """Loads a list from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("TrafficSigns", {}).get("Types", [])  # Accesses trafficsigns["types"]
    
def load_speciallane_list_from_json(file_path):
    """Loads a list from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("LaneInformation", {}).get("SpecialLanes", [])  # Accesses trafficsigns["types"]

def load_vehicletype_list_from_json(file_path):
    """Loads a list from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("Vehicles", {}).get("VehicleTypes", [])  # Accesses trafficsigns["types"]
    
def load_vehiclestate_list_from_json(file_path):
    """Loads a list from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("Vehicles", {}).get("States", [])  # Accesses trafficsigns["types"]
    
def load_egodirection_list_from_json(file_path):
    """Loads a list from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("Ego-Vehicle", {}).get("Direction", [])  # Accesses trafficsigns["types"]
    
def load_egomaneuver_list_from_json(file_path):
    """Loads a list from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("Ego-Vehicle", {}).get("Maneuver", [])  # Accesses trafficsigns["types"]

def compare_lists(list1, list2):
    """Compares two lists and returns common and unique items."""
    set1, set2 = set(map(str, list1)), set(map(str, list2))
    common_items = set1.intersection(set2)
    unique_to_list1 = set1 - set2
    unique_to_list2 = set2 - set1

    
    return {
        "common_items": sorted(common_items),
        "unique_to_list1": sorted(unique_to_list1),
        "unique_to_list2": sorted(unique_to_list2)
    }

# Path to the JSON file
json_file_path = '/media/william/blueicedrive/Github/UDrive/Analysis/Overall.json'

# Load the list from the JSON file
list_from_json = load_trafficsigns_list_from_json(json_file_path)

# Define the other list for comparison
other_list = ['Yield Sign', 'Curve', 'Pedestrian Crossing', 'Directional Arrow', 'Traffic Light', 'Pedestrian Signal', 'No Parking', 'Parking Sign', 'NoTrafficSigns', 'Do Not Enter', 'Construction Warning', 'Bus Stop Sign', 'Pedestrian Zone', 'One Way Sign', 'NoSign', 'Warning Sign', 'Stop Sign', 'Information Sign', 'Speed Limit', 'Pedestrian Crossing Sign', 'Directional Sign', 'No Entry', 'Bike Lane Sign', 'Yield', 'Speed Limit 30', 'Street Sign', 'No Trucks Allowed', 'Keep Right Sign', 'No Left Turn', 'Pedestrian Warning', 'One-Way Sign', 'Gas Station Sign', 'Lane Direction Sign', 'Bicycle Lane Sign', 'No Entry Sign', 'No U-Turn', 'Detour', 'Weight Limit', 'Road Work', 'Electronic Sign', 'Height Limit', 'Bus Lane', 'Taxi and Bus Lane', 'Public Transport Sign', 'One Way', 'Emergency Route', 'TrafficLight', 'Bicycle Crossing', 'Speed Limit 40 km/h', 'Weight Limit 3.3t', 'One-Way Street', 'Parking', 'Tow Area Sign', 'Taxi Sign', 'Intersection Warning', 'One-Way', 'Hospital Sign', 'Bicycle Sign', 'Roundabout', 'Tunnel Sign', 'Merge Sign', 'Priority Road', 'Dead End', 'Two-Way Traffic', 'Left Turn Only']

comparison_result = compare_lists(list_from_json, other_list)

# Display the results
# print("Common items:", comparison_result["common_items"])
print("Unique in Traffic Signs items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# special lanes
list_from_json = load_speciallane_list_from_json(json_file_path)
other_list = ['NoSpecialLanes', 'Bike Lane', 'Street Parking', 'Crosswalk', 'Bus Lane', 'Right Turn Only Lane', 'Left Turn Only Lane', 'Tram Tracks', 'Construction Barriers', 'Turn Lane', 'Bicycle Lane', 'Bus Stop', 'Forward Only Lane', 'Bridge', 'Roundabout', 'Traffic Cones Blocking Parts of the Road', 'Directional Arrow', 'Pedestrian Walkway', 'Construction Zone', 'Parking Lane', 'Bus Stop Sign', 'Taxi and Bus Lane', 'Turning Lane', 'Parking Sign', 'Tram Lane', 'BicycleLane']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in Special Lanes items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# vehicle type
list_from_json = load_vehicletype_list_from_json(json_file_path)
other_list = ['SUV', 'Sedan', 'Taxi', 'Hatchback', 'Van', 'Motorcycle', 'Ambulance', 'Bus', 'Compact Car', 'NoVehicleType', 'Station Wagon', 'Delivery Truck', 'Trolley', 'Tram', 'Truck', 'Construction Vehicles', 'Convertible', 'Bicycle', 'Scooter', 'Minivan', 'Sports Car', 'Electric Vehicle', 'Cars', 'Police Car', 'Pickup Truck', 'RV', 'Tour Bus', 'Camper Van', 'Classic Car', 'Bicycles']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in vehicle type items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))


# vehicle state
list_from_json = load_vehiclestate_list_from_json(json_file_path)
other_list = ['In Motion', 'Turning', 'Parked', 'Stopped', 'Stopped at Traffic Light', 'In Queue', 'Merging', 'Turning Right', 'Waiting to Turn', 'NoVehicleState', 'Door Open', 'Moving', 'Blocking Parts of the Road', 'Waiting', 'Stopped at Bus Stop', 'Loading', 'Stopped at Intersection', 'Waiting to Turn Left', 'Overtaking', 'Stopped at Crosswalk', 'Turning Left', 'Following', 'Slowing Down', 'Stopped at Stop Sign']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in vehcile state items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))


# ego direction
list_from_json = load_egodirection_list_from_json(json_file_path)
other_list = ['EgoEgoApproaching Roundabout', "Ego['EgoForward']", 'EgoEgoStopped at Traffic Light', "Ego['EgoStopped']", 'EgoEgoStopped', 'EgoEgoForward', "Ego['EgoStopped at Intersection']", 'EgoEgoApproaching Intersection', 'EgoEgoRight', 'EgoEgoMaking a Left Turn', 'EgoEgoMaking a Right Turn', 'EgoEgoMerging', 'EgoEgoMerging ', 'EgoEgoStopped at Intersection', 'EgoEgoStopped at Crosswalk', 'EgoEgoIn Queue', 'EgoEgoExiting Roundabout', 'EgoEgoTurning', 'EgoEgoMoving', 'EgoEgoEntering Roundabout']
print("Unique in ego direction items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# ego maneuver
list_from_json = load_egomaneuver_list_from_json(json_file_path)
other_list = ['EgoEgoMoving', "Ego['EgoMoving']", 'EgoEgoFullStopped', "Ego['EgoFullStopped']", "Ego['EgoWaiting']", 'EgoEgoSlowing Down', 'EgoEgoWaiting', 'EgoEgoProceeding through Intersection', 'EgoEgoTurningRight', 'EgoEgoStopped', 'EgoEgoTurning Left', 'EgoEgoTurning Right', 'EgoEgoMerging Left', 'EgoEgoFollowing', 'EgoEgoIn Queue', 'EgoEgoYielding', 'EgoEgoProceeding', 'EgoEgoSlowing', 'EgoEgoMerging Right', 'EgoEgoMovingForward']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in ego maneuver items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))





