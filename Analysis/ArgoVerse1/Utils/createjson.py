import os
import json

def build_json_structure(root_folder):
    """
    Build a nested JSON structure for the folder structure, including image filenames.
    :param root_folder: The root folder to start the traversal from.
    :return: A nested dictionary reflecting the folder structure with image filenames.
    """
    structure = {}
    for sceneid in sorted(os.listdir(root_folder)):
        scene_path = os.path.join(root_folder, sceneid)
        if os.path.isdir(scene_path):
            images = []
            for filename in sorted(os.listdir(scene_path)):
                file_path = os.path.join(scene_path, filename)
                if os.path.isfile(file_path):  # Check if it's a file to include as an imageid
                    images.append({"id": filename, "value": {}})
            structure[sceneid] = images
    return structure

def save_json(structure, file_path):
    """
    Save the nested dictionary structure as a JSON file including image filenames.
    :param structure: The nested dictionary to save.
    :param file_path: The path to the JSON file to save the structure to.
    """
    with open(file_path, 'w') as json_file:
        json.dump(structure, json_file, indent=4)



root_folder = "/home/carla/Github/UDrive/Analysis/ArgoVerse1/images"  # Adjust this path as necessary
structure = build_json_structure(root_folder)
json_file_path = "/home/carla/Github/UDrive/Analysis/ArgoVerse1/Analysis.json"  # Name of the JSON file to save
save_json(structure, json_file_path)

print(f"JSON file created at {json_file_path} with the folder structure.")
