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
other_list = ['NoTrafficSigns', 'Pedestrian Crossing', 'Route Sign', 'No Parking', 'Construction Warning', 'Road Work Ahead', 'One Way Sign', 'Stop Sign', 'Speed Limit', 'Parking Sign', 'No Right Turn', 'Two-Way Traffic', 'Railroad Crossing', 'Road Work', 'Detour', 'Traffic Light', 'No Left Turn', 'No Turn On Red', 'Left Lane Must Turn Left', 'Yield Sign', 'Bus Stop Sign', 'Crosswalk', 'Exit Sign', 'Bike Lane Sign', 'Road Closed', 'Electronic Sign', 'No U-Turn', 'Left Turn Only', 'Right Turn Only', 'Crosswalk Closed', 'Directional Arrow', 'Work Zone', 'Speeding Fine Doubled', 'Merge Sign', 'End Road Work', 'Double Fines End', 'Keep Right Sign', 'Do Not Enter', 'No Stopping', 'Street Sign', 'No Trucks Allowed', 'Stop for Pedestrians', 'Weight Limit', 'Share the Road', 'Right Lane Must Turn Right', 'Pedestrian Signal', 'No Pedestrian Crossing', 'Traffic Light Warning Sign', 'Pedestrian Warning', 'Do Not Block', 'Do Not Block Intersection', 'Tow Area Sign', 'Yield to Pedestrians', 'School Zone', 'Fallen Sign', 'Bus Lane', 'Curve', 'Loading Zone Sign', 'Do Not Stop on Tracks', 'Bike Lane Ends', 'NoSign', 'Information Sign', 'Not a Thru Street']

comparison_result = compare_lists(list_from_json, other_list)

# Display the results
# print("Common items:", comparison_result["common_items"])
print("Unique in Traffic Signs items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# special lanes
list_from_json = load_speciallane_list_from_json(json_file_path)
other_list = ['Street Parking', 'NoSpecialLanes', 'Crosswalk', 'Bike Lane', 'Right Turn Only Lane', 'Road Work', 'Taxi and Bus Lane', 'Center Lane', 'Left Turn Only Lane', 'Forward Only Lane', 'Traffic Cones Blocking Parts of the Road', 'None', 'Construction Cones', 'Bridge', 'Roundabout', 'Construction Barriers']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in Special Lanes items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# vehicle type
list_from_json = load_vehicletype_list_from_json(json_file_path)
other_list = ['Pickup Truck', 'Van', 'Sedan', 'SUV', 'Truck', 'Construction Vehicles', 'Service Vehicle', 'Utility Truck', 'Compact Car', 'Cars', 'Commercial Delivery Truck', 'NoVehicleType', 'Bus', 'Commercial Vehicle', 'Minivan', 'Delivery Truck', 'Semi-Trailer Truck', 'Box Truck', 'Motorcycle', 'Taxi', 'Hatchback', 'Ambulance', 'Cement Mixer Truck', 'Trolley', 'Police Car', 'Jeep', 'Coupe', 'Crossover', 'Sports Car', 'Convertible', 'Forklift', 'RV', 'Commerical Truck', 'Armored Truck', 'Containers', 'Shuttle Bus']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in vehicle type items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))


# vehicle state
list_from_json = load_vehiclestate_list_from_json(json_file_path)
other_list = ['Parked', 'In Motion', 'NoVehicleState', 'Blocking Parts of the Road', 'Stopped', 'In Queue', 'Stopped at Intersection', 'Turning', 'Violate Traffic Rules', 'Turning Left', 'Merging', 'Passenger Exiting', 'Waiting', 'Waiting to Turn Right', 'Slowing Down', 'Door Open', 'Utility Work', 'Picking up a Passenger', 'Turning Right', 'Crossing Intersection', 'Waiting to Turn Left', 'Waiting to Turn', 'Exiting Intersection', 'Loading', 'Performing Roadwork', 'Interacting with Driver', 'Stopped at Traffic Light']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in vehcile state items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))


# ego direction
list_from_json = load_egodirection_list_from_json(json_file_path)
other_list = ['EgoForward', 'EgoMaking a Right Turn', 'EgoStopped at Intersection', 'EgoMaking a Left Turn', 'EgoApproaching Intersection', 'EgoMerging Right', 'EgoMerging Left', 'EgoApproaching Roundabout', 'EgoExiting Roundabout', 'EgoStopped', 'EgoStopped at Stop Sign', 'EgoParked', 'EgoEntering Roundabout']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in ego direction items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))

# ego maneuver
list_from_json = load_egomaneuver_list_from_json(json_file_path)
other_list = ['EgoMoving', 'EgoTurning Right', 'EgoTurning Left', 'EgoSlowing Down', 'EgoWaiting', 'EgoFollowing', 'EgoFullStopped', 'EgoIn Queue', 'EgoMerging Left', 'EgoMerging', 'EgoProceeding through Intersection', 'EgoYielding', 'EgoOvertaking on Opposing Lane', 'EgoOvertaking', 'EgoStopped in Parking Space']
comparison_result = compare_lists(list_from_json, other_list)
print("Unique in ego maneuver items:", comparison_result["unique_to_list2"], "Length: ", len(comparison_result["unique_to_list2"]))





