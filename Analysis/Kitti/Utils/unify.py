import json

file = "/media/william/blueicedrive/Github/UDrive/Analysis/nuScenes/Analysis.json"
traffic_signs_list = []
speciallanes_list = []
vehicletype_list = []
vehiclestate_list = []
egodirection_list = []
egomaneuver_list = []

with open(file, 'r') as file:
    data = json.load(file)

def str2list(x):
    if isinstance(x, str):
        x = x.split(",")
    return x
unified_data = {}
for image_name, image_analysis in data.items():
    try:
        Scene = image_analysis["Scene"]                                    # this is always a string
    except:
        print(image_name, "scene")
    try:
        TimeOfDay = image_analysis["TimeOfDay"]                            # this is always a string
    except KeyError:
        print(image_name, "time")
    try:
        Weather = image_analysis["Weather"]                               # this is always a string
    except KeyError:
        print(image_name, "weather")
    
    if Weather == "Not Indicated":
        image_analysis["Weather"] = "NoWeatherCondition"
    RoadConditions = image_analysis["RoadConditions"]                  # this is always a string
    try:
        NumberOfLanes = image_analysis["LaneInformation"]["NumberOfLanes"] # this is always a string
    except KeyError:
        print(image_name, "numoflane")
    if NumberOfLanes == "Multiple":
        image_analysis["LaneInformation"]["NumberOfLanes"] = "MultipleLanes"
    elif NumberOfLanes == "1":
        image_analysis["LaneInformation"]["NumberOfLanes"] = "One"
    elif NumberOfLanes == "2":
        image_analysis["LaneInformation"]["NumberOfLanes"] = "Two"
    elif NumberOfLanes == "3":
        image_analysis["LaneInformation"]["NumberOfLanes"] = "Three"
    elif NumberOfLanes == "4":
        image_analysis["LaneInformation"]["NumberOfLanes"] = "Four"
    elif NumberOfLanes == "5":
        image_analysis["LaneInformation"]["NumberOfLanes"] = "Five"
    LaneMarkings = image_analysis["LaneInformation"]["LaneMarkings"]   # this is always a string
    if LaneMarkings == "Visible":
        image_analysis["LaneInformation"]["LaneMarkings"] = "LaneVisible"
    elif LaneMarkings == "Not Clearly Visible":
        image_analysis["LaneInformation"]["LaneMarkings"] = "Lane Not Clearly Visible"
    SpecialLanes = image_analysis["LaneInformation"]["SpecialLanes"]   # this is always a list
    if isinstance(SpecialLanes, str):
        SpecialLanes = SpecialLanes.split(",")
        image_analysis["LaneInformation"]["SpecialLanes"] = SpecialLanes
    if len(SpecialLanes) == 1 and SpecialLanes[0] == "None":
        SpecialLanes[0] = "NoSpecialLanes"
        image_analysis["LaneInformation"]["SpecialLanes"] = SpecialLanes
    for x in SpecialLanes:
        if x == "Pedestrian Crossing":
            print(image_name)
        if x not in speciallanes_list:
            speciallanes_list.append(x)


    try:
        TrafficSignsTypes = image_analysis["TrafficSigns"]["Types"]        # this is always a list   
    except KeyError:
        print(image_name, "trafficsign")
    if isinstance(TrafficSignsTypes, str):
        TrafficSignsTypes = TrafficSignsTypes.split(",")
        image_analysis["TrafficSigns"]["Types"] = TrafficSignsTypes
    if "Bike Lane" in TrafficSignsTypes:
        for x in range(0, len(TrafficSignsTypes)):
            if TrafficSignsTypes[x] == "Bike Lane":
                TrafficSignsTypes[x] = "Bike Lane Sign"
            elif TrafficSignsTypes[x] == "Bus Stop":
                TrafficSignsTypes[x] = "Bus Stop Sign"
        image_analysis["TrafficSigns"]["Types"] = TrafficSignsTypes
    if "Bus Stop" in TrafficSignsTypes:
        for x in range(0, len(TrafficSignsTypes)):
            if TrafficSignsTypes[x] == "Bus Stop":
                TrafficSignsTypes[x] = "Bus Stop Sign"
        image_analysis["TrafficSigns"]["Types"] = TrafficSignsTypes
    if len(TrafficSignsTypes) == 1 and TrafficSignsTypes[0] == "None":
        TrafficSignsTypes[0] = "NoTrafficSigns"
        image_analysis["TrafficSigns"]["Types"] = TrafficSignsTypes
    if TrafficSignsTypes == "" or TrafficSignsTypes == []:
        TrafficSignsTypes = ["NoTrafficSigns"]
        image_analysis["TrafficSigns"]["Types"] = TrafficSignsTypes
    for x in TrafficSignsTypes:
        if x not in traffic_signs_list:
            traffic_signs_list.append(x)
    if "Traffic Light" in TrafficSignsTypes and "TrafficLightState" not in  image_analysis["TrafficSigns"]:
        print("missing traffic light state", image_name)
        if "TrafficLightState" in image_analysis:
            image_analysis["TrafficSigns"]["TrafficLightState"] = image_analysis["TrafficLightState"]
        else:
            print("traffic light visible but traffic light state missing entirely", image_name)
    temp = image_analysis["TrafficSigns"]["Types"]
    del image_analysis["TrafficSigns"]["Types"]
    image_analysis["TrafficSigns"]["TrafficSignsTypes"] = temp
    
    try:
        TrafficSignsVisibility = image_analysis["TrafficSigns"]["Visibility"]   # this is always a string
        if TrafficSignsVisibility == "None":
            image_analysis["TrafficSigns"]["Visibility"] = "NoTrafficSigns"
        elif TrafficSignsVisibility == "Not Visible":
            image_analysis["TrafficSigns"]["Visibility"] = "SignNotVisible"
    except KeyError:
        print(image_name, "trafficsign")
    if len(image_analysis["TrafficSigns"]) == 3:
        try:
            TrafficSignsTrafficLightState = image_analysis["TrafficSigns"]["TrafficLightState"] # this is always a string
        except KeyError:
            print(image_name, "trafficlighstate")
    temp = image_analysis["TrafficSigns"]["Visibility"]
    del image_analysis["TrafficSigns"]["Visibility"]
    image_analysis["TrafficSigns"]["TrafficSignsVisibility"] = temp

    
    VehiclesTotalNumber = image_analysis["Vehicles"]["TotalNumber"]        # string
    if VehiclesTotalNumber == "None":
        VehiclesTotalNumber = "NoVehicle"
        image_analysis["Vehicles"]["TotalNumber"] = VehiclesTotalNumber
    elif VehiclesTotalNumber == "Multiple":
        image_analysis["Vehicles"]["TotalNumber"] = "MultipleVehicles"
    
    try:
        VehiclesInMotion = image_analysis["Vehicles"]["InMotion"]              # list
        if isinstance(VehiclesInMotion, str):
            VehiclesInMotion = VehiclesInMotion.split(",")
            image_analysis["Vehicles"]["InMotion"] = VehiclesInMotion
    except KeyError:
        print(image_name, "inmotion")
    try:
        VehiclesTypes = image_analysis["Vehicles"]["VehicleTypes"]                    # list
        if isinstance(VehiclesTypes, str):
            VehiclesTypes = VehiclesTypes.split(",")
            image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes   
        if len(VehiclesTypes) == 1 and VehiclesTypes[0] == "None":
            VehiclesTypes[0] = "NoVehicleType"
            image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes
        if len(VehiclesTypes) == 0:
            VehiclesTypes = ["NoVehicleType"]
            image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes
        temp = image_analysis["Vehicles"]["VehicleTypes"]
        del image_analysis["Vehicles"]["VehicleTypes"]
        image_analysis["TrafficSigns"]["VehicleTypes"] = temp
    except KeyError:
        # print(image_name)
        VehiclesTypes = image_analysis["Vehicles"]["Types"]
        del image_analysis["Vehicles"]["Types"]
        image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes
        
        if isinstance(VehiclesTypes, str):
            VehiclesTypes = VehiclesTypes.split(",")
            image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes   
        if len(VehiclesTypes) == 1 and VehiclesTypes[0] == "None":
            VehiclesTypes[0] = "NoVehicleType"
            image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes
        if len(VehiclesTypes) == 0:
            VehiclesTypes = ["NoVehicleType"]
            image_analysis["Vehicles"]["VehicleTypes"] = VehiclesTypes
        # print(image_analysis["Vehicles"])
        # temp = image_analysis["Vehicles"]["VehicleTypes"]
        # del image_analysis["Vehicles"]["VehicleTypes"]
        # image_analysis["TrafficSigns"]["VehicleTypes"] = temp 
    for x in VehiclesTypes:
        if x == "Parked":
            print(image_name)
        if x not in vehicletype_list:
            vehicletype_list.append(x)
    
    try:
        VehiclesStates = image_analysis["Vehicles"]["States"]                  # list
    except KeyError:
        print(image_name, "vehicle states")
    if isinstance(VehiclesStates, str):
        VehiclesStates = VehiclesStates.split(",")
        image_analysis["Vehicles"]["States"] = VehiclesStates
    if len(VehiclesStates) == 1 and VehiclesStates[0] == "None":
        VehiclesStates[0] = "NoVehicleState"
        image_analysis["Vehicles"]["States"] = VehiclesStates
    if len(VehiclesStates) == 0:
        VehiclesStates = ["NoVehicleState"]
        image_analysis["Vehicles"]["States"] = VehiclesStates
    for x in VehiclesStates:
        if x == "Proceeding through Intersection":
            print(image_name)
        if x not in vehiclestate_list:
            vehiclestate_list.append(x)

    try:    
        Pedestrians = image_analysis["Pedestrians"]                            # list
    except KeyError:
        print(image_name)
    if isinstance(Pedestrians, str):
        Pedestrians = Pedestrians.split(",")
        image_analysis["Pedestrians"] = Pedestrians
    try:
        if len(Pedestrians) == 1 and Pedestrians[0] == "None":
            Pedestrians[0] = "NoPed"
            image_analysis["Pedestrians"] = Pedestrians
        elif Pedestrians[0] == "Multiple":
            image_analysis["Pedestrians"] = ["MultiplePed"]
    except:
        print(image_name, "ped")

    Directionality = image_analysis["Directionality"]                      # string

    image_analysis["Ego-Vehicle"]["Direction"] = "Ego"+str(image_analysis["Ego-Vehicle"]["Direction"])
    EgoVehicleDirection = image_analysis["Ego-Vehicle"]["Direction"]       # string
    if EgoVehicleDirection not in egodirection_list:
        egodirection_list.append(EgoVehicleDirection)


    image_analysis["Ego-Vehicle"]["Maneuver"] = "Ego"+str(image_analysis["Ego-Vehicle"]["Maneuver"]) 
    EgoVehicleManeuver = image_analysis["Ego-Vehicle"]["Maneuver"]         # string
    if EgoVehicleManeuver == "None":
        EgoVehicleManeuver = "EgoNoManeuver"
        image_analysis["Ego-Vehicle"]["Maneuver"] = "Ego"+EgoVehicleManeuver
    if EgoVehicleManeuver not in egomaneuver_list:
        if EgoVehicleManeuver == "Ego['Merging Left']":
            print(image_name)
        egomaneuver_list.append(EgoVehicleManeuver)

    try:
        VisibilityGeneral = image_analysis["Visibility"]["General"]            # string
    except:
        print(image_name, "visgeneral")

    if len(image_analysis["Visibility"]) == 2:
        VisibilitySpecificImpairments = image_analysis["Visibility"]["SpecificImpairments"] # list
        if isinstance(VisibilitySpecificImpairments, str):
            VisibilitySpecificImpairments = VisibilitySpecificImpairments.split(",")
            image_analysis["Visibility"]["SpecificImpairments"] = VisibilitySpecificImpairments
        if len(VisibilitySpecificImpairments) == 1 and VisibilitySpecificImpairments[0] == "None":
            VisibilitySpecificImpairments[0] = "NoImpairments"
            image_analysis["Visibility"]["SpecificImpairments"] = VisibilitySpecificImpairments
        if len(VisibilitySpecificImpairments) == 0:
            VisibilitySpecificImpairments = ["NoImpairments"]
            image_analysis["Visibility"]["SpecificImpairments"] = VisibilitySpecificImpairments

    try:
        CameraCondition = image_analysis["CameraCondition"]                  # string
    except KeyError:
        print(image_name, "camcondition")

    Severity = image_analysis["Severity"]                                      # integer

    try:
        policeman = image_analysis["Policeman"]
        police_present = image_analysis["Policeman"]["Presence"]
        if police_present == "False":
            del image_analysis["Policeman"]
        elif police_present == "True":
            image_analysis["Policeman"]["Presence"] = "PolicemanPresent"

    except:
        pass

    try:
        bicyclist = image_analysis["Bicyclist"]
        if bicyclist == "None":
            del image_analysis["Bicyclist"]
        bicyclist_present = image_analysis["Bicyclist"]["Presence"]
        if bicyclist_present == "False" or bicyclist_present == "None" or bicyclist_present == "":
            del image_analysis["Bicyclist"]
        elif police_present == "True":
            image_analysis["Bicyclist"]["Presence"] = "BicyclistPresent"
    except:
        pass

    try:
        animals = image_analysis["Animals"] 
        if animals == "None":
            del image_analysis["Animals"]
        animal_present = image_analysis["Animals"]["Presence"]
        if animal_present == "False" or animal_present == "None":
            del image_analysis["Animals"]
        elif animal_present == "True":
            animal_present = image_analysis["Animals"]["Presence"] == "AnimalPresent"
    except:
        pass

    try: 
        if image_analysis["Animals"]["Type"] == "None" or image_analysis["Animals"]["Type"] == [] or image_analysis["Animals"]["Type"] == "":
            del image_analysis["Animals"]
    except:
        pass

print(f"Traffic list: {traffic_signs_list}")
print(f"Speciallanes list: {speciallanes_list}")
print(f"VehicleType list: {vehicletype_list}")
print(f"VehicleState list: {vehiclestate_list}")
print(f"EgoDirection list: {egodirection_list}")
print(f"EgoManeuver list: {egomaneuver_list}")

with open("/media/william/blueicedrive/Github/UDrive/Analysis/nuScenes/unifiedAnalysis.json", "w") as outfile:
    json.dump(data, outfile)