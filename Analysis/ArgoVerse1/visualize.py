import json

file = "/home/carla/Github/UDrive/Analysis/ArgoVerse1/prelinminaryanalysis.json"

with open(file, 'r') as file:
    data = json.load(file)

def str2list(x):
    if isinstance(x, str):
        x = x.split(",")
    return x

for scenario_name, image_list in data.items():
    # print(scenario_name)
    for image_analysis in image_list:
        # print(image_analysis) 
        id = image_analysis["id"]                                                   # this is always a string
        Scene = image_analysis["value"]["Scene"]                                    # this is always a string
        TimeOfDay = image_analysis["value"]["TimeOfDay"]                            # this is always a string
        Weather = image_analysis["value"]["Weather"]                                # this is always a string
        RoadConditions = image_analysis["value"]["RoadConditions"]                  # this is always a string
        NumberOfLanes = image_analysis["value"]["LaneInformation"]["NumberOfLanes"] # this is always a string
        LaneMarkings = image_analysis["value"]["LaneInformation"]["LaneMarkings"]   # this is always a string
        
        SpecialLanes = image_analysis["value"]["LaneInformation"]["SpecialLanes"]   # this is always a list
        if isinstance(SpecialLanes, str):
            SpecialLanes = SpecialLanes.split(",")
        
        TrafficSignsTypes = image_analysis["value"]["TrafficSigns"]["Types"]        # this is always a list
        if isinstance(TrafficSignsTypes, str):
            TrafficSignsTypes = TrafficSignsTypes.split(",")
        
        TrafficSignsVisibility = image_analysis["value"]["TrafficSigns"]["Visibility"]   # this is always a string
        if len(image_analysis["value"]["TrafficSigns"]) == 3:
            TrafficSignsTrafficLightState = image_analysis["value"]["TrafficSigns"]["TrafficLightState"] # this is always a string
        
        VehiclesTotalNumber = image_analysis["value"]["Vehicles"]["TotalNumber"]        # string
        
        VehiclesInMotion = image_analysis["value"]["Vehicles"]["InMotion"]              # list
        if isinstance(VehiclesInMotion, str):
            VehiclesInMotion = VehiclesInMotion.split(",")
        
        VehiclesTypes = image_analysis["value"]["Vehicles"]["Types"]                    # list
        if isinstance(VehiclesTypes, str):
            VehiclesTypes = VehiclesTypes.split(",")                   
        
        VehiclesStates = image_analysis["value"]["Vehicles"]["States"]                  # list
        if isinstance(VehiclesStates, str):
            VehiclesStates = VehiclesStates.split(",")

        Pedestrians = image_analysis["value"]["Pedestrians"]                            # list
        if isinstance(Pedestrians, str):
            Pedestrians = Pedestrians.split(",")

        Directionality = image_analysis["value"]["Directionality"]                      # string

        EgoVehicleDirection = image_analysis["value"]["Ego-Vehicle"]["Direction"]       # string

        EgoVehicleManeuver = image_analysis["value"]["Ego-Vehicle"]["Maneuver"]         # string

        VisibilityGeneral = image_analysis["value"]["Visibility"]["General"]            # string
        if len(image_analysis["value"]["Visibility"]) == 2:
            VisibilitySpecificImpairments = image_analysis["value"]["Visibility"]["SpecificImpairments"] # list
            if isinstance(VisibilitySpecificImpairments, str):
                VisibilitySpecificImpairments = VisibilitySpecificImpairments.split(",")

        
        if isinstance(VisibilitySpecificImpairments, str) == False:
            print(VisibilitySpecificImpairments)