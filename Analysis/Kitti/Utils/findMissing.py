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
other_list = ['NoTrafficSigns', 'Pedestrian Crossing', 'Speed Limit', 'Directional Arrow', 'Warning Sign', 'Parking Sign', 'Exit Sign', 'Yield Sign', 'Weight Limit', 'Road Work Ahead', 'No Parking', 'Traffic Light', 'No Entry', 'Dead End', 'Stop Sign', 'Road Work', 'Bus Stop Sign', 'Height Limit', 'Railroad Crossing', 'Merge Sign', 'Information Sign', 'Do Not Enter', 'Street Sign', 'Bike Lane Sign', 'Priority Road', 'Curve', 'Tram Sign', 'Keep Right Sign', 'Construction Warning', 'Pedestrian Warning', 'Loading Zone', 'Pedestrian Signal', 'Speed Bump', 'Direction Sign', 'Priority Road Sign', 'Speed Limit Sign', 'No Entry Sign', 'No Trucks Allowed', 'NoSign', 'No Vehicles Allowed', 'One-Way Sign']

comparison_result = compare_lists(list_from_json, other_list)

# Display the results
# print("Common items:", comparison_result["common_items"])
print("Unique in Traffic Signs items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# special lanes
list_from_json = load_speciallane_list_from_json(json_file_path)
other_list = ['NoSpecialLanes', 'Street Parking', 'Tram Tracks', 'Crosswalk', 'Traffic Cones Blocking Parts of the Road', 'Bike Lane', ' Street Parking', 'Left Turn Only Lane', 'Forward Only Lane', 'Right Turn Only Lane', 'Road Work', 'Construction Cones', 'Construction Barriers', ' Tram Tracks', 'Bridge', 'Roundabout', 'Bus Lane', 'Exit Sign', 'Exit Lane', 'Median', 'Center Lane', 'Bus Stop', 'Bus Stop Sign', 'Divided']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in Special Lanes items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# vehicle type
list_from_json = load_vehicletype_list_from_json(json_file_path)
other_list = ['NoVehicleType', 'Sedan', 'Hatchback', 'Convertible', 'Vans', 'Compact Car', 'Bus', 'SUV', 'Taxi', 'Van', 'Truck', 'Commercial Vehicle', 'Commercial Truck', 'Cars', 'Minivan', 'Utility Truck', 'Commercial Delivery Truck', 'Construction Vehicles', 'Trolley', 'Tram', 'Station Wagon', 'Motorcycle', 'Trailer', 'Camper', 'Semi-Trailer Truck', 'Sports Car', 'Bicycle', 'RV', 'Pickup Truck', 'Delivery Truck', 'Box Truck', 'Police Car', 'Smart Car', 'Jeep', 'Scooter', 'Classic Car']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in vehicle type items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))


# vehicle state
list_from_json = load_vehiclestate_list_from_json(json_file_path)
other_list = ['NoVehicleState', 'Parked', 'In Motion', 'Door Open', 'Stopped', 'Passenger Exiting', 'Stopped at Intersection', 'Merging', 'Blocking Parts of the Road', 'In Queue', 'Crossing Intersection', 'Waiting to Turn', 'Stopped at Traffic Light', 'Waiting', 'Waiting at Traffic Light', 'Loading/Unloading', 'Waiting to Turn Right', 'Stopped at Crosswalk', 'Turning Left']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in vehcile state items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))


# ego direction
list_from_json = load_egodirection_list_from_json(json_file_path)
other_list = ['EgoUnknown', 'EgoForward', 'EgoMaking a Left Turn', 'EgoMaking a Right Turn', 'EgoForward', 'EgoStopped', 'EgoApproaching Intersection', 'EgoStopped at Traffic Light', 'EgoMaking a Left Turn', 'EgoParked', 'EgoApproaching Roundabout', 'EgoStopped in Parking Space', 'EgoMaking a Right Turn', 'EgoExiting Highway', 'EgoRight']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in ego direction items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# ego maneuver
list_from_json = load_egomaneuver_list_from_json(json_file_path)
other_list = ['EgoUnknown', 'EgoMoving', 'EgoFollowing', 'EgoTurning', 'EgoSlowing Down', 'EgoTurning right', 'EgoStopped', 'EgoProceeding through intersection', 'EgoIn Queue', 'EgoMoving', 'EgoFullStopped', 'EgoProceeding through Intersection', 'EgoStopped in Parking Space', 'EgoFollowing', 'EgoStopped at Traffic Light', 'EgoTurning Left', 'EgoIn Queue', 'EgoSlowing Down', 'EgoTurning Right', 'EgoWaiting', 'EgoTurningRight', 'EgoYielding']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in ego maneuver items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))





