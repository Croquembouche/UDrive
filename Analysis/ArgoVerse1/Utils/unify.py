import json

file = "/home/carla/Github/UDrive/Analysis/ArgoVerse1/Analysis.json"

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
        try:
            Scene = image_analysis["value"]["Scene"]                                    # this is always a string
        except KeyError:
            print(id)
        try:
            TimeOfDay = image_analysis["value"]["TimeOfDay"]                            # this is always a string
        except KeyError:
            print(id)
        Weather = image_analysis["value"]["Weather"]                               # this is always a string
        if Weather == "Not Indicated":
            image_analysis["value"]["Weather"] = "NoWeatherCondition"
        RoadConditions = image_analysis["value"]["RoadConditions"]                  # this is always a string
        NumberOfLanes = image_analysis["value"]["LaneInformation"]["NumberOfLanes"] # this is always a string
        if NumberOfLanes == "Multiple":
            image_analysis["value"]["LaneInformation"]["NumberOfLanes"] = "MultipleLanes"
        elif NumberOfLanes == "1":
            image_analysis["value"]["LaneInformation"]["NumberOfLanes"] = "One"
        elif NumberOfLanes == "2":
            image_analysis["value"]["LaneInformation"]["NumberOfLanes"] = "Two"
        elif NumberOfLanes == "3":
            image_analysis["value"]["LaneInformation"]["NumberOfLanes"] = "Three"
        elif NumberOfLanes == "4":
            image_analysis["value"]["LaneInformation"]["NumberOfLanes"] = "Four"
        elif NumberOfLanes == "5":
            image_analysis["value"]["LaneInformation"]["NumberOfLanes"] = "Five"
        LaneMarkings = image_analysis["value"]["LaneInformation"]["LaneMarkings"]   # this is always a string
        if LaneMarkings == "Visible":
            image_analysis["value"]["LaneInformation"]["LaneMarkings"] = "LaneVisible"
        elif LaneMarkings == "Not Clearly Visible":
            image_analysis["value"]["LaneInformation"]["LaneMarkings"] = "Lane Not Clearly Visible"
        SpecialLanes = image_analysis["value"]["LaneInformation"]["SpecialLanes"]   # this is always a list
        if isinstance(SpecialLanes, str):
            SpecialLanes = SpecialLanes.split(",")
            image_analysis["value"]["LaneInformation"]["SpecialLanes"] = SpecialLanes
        if len(SpecialLanes) == 1 and SpecialLanes[0] == "None":
            SpecialLanes[0] = "NoSpecialLanes"
            image_analysis["value"]["LaneInformation"]["SpecialLanes"] = SpecialLanes
        
        TrafficSignsTypes = image_analysis["value"]["TrafficSigns"]["Types"]        # this is always a list
        if isinstance(TrafficSignsTypes, str):
            TrafficSignsTypes = TrafficSignsTypes.split(",")
            image_analysis["value"]["TrafficSigns"]["Types"] = TrafficSignsTypes
        if "Bike Lane" in TrafficSignsTypes:
            for x in range(0, len(TrafficSignsTypes)):
                if TrafficSignsTypes[x] == "Bike Lane":
                    TrafficSignsTypes[x] = "Bike Lane Sign"
                elif TrafficSignsTypes[x] == "Bus Stop":
                    TrafficSignsTypes[x] = "Bus Stop Sign"
            image_analysis["value"]["TrafficSigns"]["Types"] = TrafficSignsTypes
        if "Bus Stop" in TrafficSignsTypes:
            for x in range(0, len(TrafficSignsTypes)):
                if TrafficSignsTypes[x] == "Bus Stop":
                    TrafficSignsTypes[x] = "Bus Stop Sign"
            image_analysis["value"]["TrafficSigns"]["Types"] = TrafficSignsTypes
        if len(TrafficSignsTypes) == 1 and TrafficSignsTypes[0] == "None":
            TrafficSignsTypes[0] = "NoTrafficSigns"
            image_analysis["value"]["TrafficSigns"]["Types"] = TrafficSignsTypes
        temp = image_analysis["value"]["TrafficSigns"]["Types"]
        del image_analysis["value"]["TrafficSigns"]["Types"]
        image_analysis["value"]["TrafficSigns"]["TrafficSignsTypes"] = temp
        
        try:
            TrafficSignsVisibility = image_analysis["value"]["TrafficSigns"]["Visibility"]   # this is always a string
            if TrafficSignsVisibility == "None":
                image_analysis["value"]["TrafficSigns"]["Visibility"] = "NoSign"
            elif TrafficSignsVisibility == "Not Visible":
                image_analysis["value"]["TrafficSigns"]["Visibility"] = "SignNotVisible"
        except KeyError:
            print(id)
        if len(image_analysis["value"]["TrafficSigns"]) == 3:
            TrafficSignsTrafficLightState = image_analysis["value"]["TrafficSigns"]["TrafficLightState"] # this is always a string
        temp = image_analysis["value"]["TrafficSigns"]["Visibility"]
        del image_analysis["value"]["TrafficSigns"]["Visibility"]
        image_analysis["value"]["TrafficSigns"]["TrafficSignsVisibility"] = temp

        
        VehiclesTotalNumber = image_analysis["value"]["Vehicles"]["TotalNumber"]        # string
        if VehiclesTotalNumber == "None":
            VehiclesTotalNumber = "NoVehicle"
            image_analysis["value"]["Vehicles"]["TotalNumber"] = VehiclesTotalNumber
        elif VehiclesTotalNumber == "Multiple":
            image_analysis["value"]["Vehicles"]["TotalNumber"] = "MultipleVehicles"
        
        VehiclesInMotion = image_analysis["value"]["Vehicles"]["InMotion"]              # list
        if isinstance(VehiclesInMotion, str):
            VehiclesInMotion = VehiclesInMotion.split(",")
            image_analysis["value"]["Vehicles"]["InMotion"] = VehiclesInMotion
        
        VehiclesTypes = image_analysis["value"]["Vehicles"]["Types"]                    # list
        if isinstance(VehiclesTypes, str):
            VehiclesTypes = VehiclesTypes.split(",")
            image_analysis["value"]["Vehicles"]["Types"] = VehiclesTypes   
        if len(VehiclesTypes) == 1 and VehiclesTypes[0] == "None":
            VehiclesTypes[0] = "NoVehicleType"
            image_analysis["value"]["Vehicles"]["Types"] = VehiclesTypes  
        temp = image_analysis["value"]["Vehicles"]["Types"]
        del image_analysis["value"]["Vehicles"]["Types"]
        image_analysis["value"]["TrafficSigns"]["VehicleTypes"] = temp             
        
        VehiclesStates = image_analysis["value"]["Vehicles"]["States"]                  # list
        if isinstance(VehiclesStates, str):
            VehiclesStates = VehiclesStates.split(",")
            image_analysis["value"]["Vehicles"]["States"] = VehiclesStates
        if len(VehiclesStates) == 1 and VehiclesStates[0] == "None":
            VehiclesStates[0] = "NoVehicleState"
            image_analysis["value"]["Vehicles"]["States"] = VehiclesStates

        Pedestrians = image_analysis["value"]["Pedestrians"]                            # list
        if isinstance(Pedestrians, str):
            Pedestrians = Pedestrians.split(",")
            image_analysis["value"]["Pedestrians"] = Pedestrians
        if len(Pedestrians) == 1 and Pedestrians[0] == "None":
            Pedestrians[0] = "NoPed"
            image_analysis["value"]["Pedestrians"] = Pedestrians
        elif Pedestrians[0] == "Multiple":
            image_analysis["value"]["Pedestrians"] = ["MultiplePed"]

        Directionality = image_analysis["value"]["Directionality"]                      # string

        EgoVehicleDirection = image_analysis["value"]["Ego-Vehicle"]["Direction"]       # string

        EgoVehicleManeuver = image_analysis["value"]["Ego-Vehicle"]["Maneuver"]         # string
        if EgoVehicleManeuver == "None":
            EgoVehicleManeuver = "NoManeuver"
            image_analysis["value"]["Ego-Vehicle"]["Maneuver"] = EgoVehicleManeuver

        try:
            VisibilityGeneral = image_analysis["value"]["Visibility"]["General"]            # string
        except KeyError:
            print(id)

        if len(image_analysis["value"]["Visibility"]) == 2:
            VisibilitySpecificImpairments = image_analysis["value"]["Visibility"]["SpecificImpairments"] # list
            if isinstance(VisibilitySpecificImpairments, str):
                VisibilitySpecificImpairments = VisibilitySpecificImpairments.split(",")
                image_analysis["value"]["Visibility"]["SpecificImpairments"] = VisibilitySpecificImpairments
            if len(VisibilitySpecificImpairments) == 1 and VisibilitySpecificImpairments[0] == "None":
                VisibilitySpecificImpairments[0] = "NoImpairments"
                image_analysis["value"]["Visibility"]["SpecificImpairments"] = VisibilitySpecificImpairments

        try:
            CameraCondition = image_analysis["value"]["CameraCondition"]                  # string
        except KeyError:
            print(id)

        Severity = image_analysis["value"]["Severity"]                                      # integer
with open("unifiedAnalysis.json", "w") as outfile:
    json.dump(data, outfile)