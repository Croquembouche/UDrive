import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from node2vec import Node2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from itertools import combinations


# Load your data
file_path = '/home/carla/Github/UDrive/unifiedAnalysis.json'  # Update this with the actual file path
with open(file_path, 'r') as file:
    data = json.load(file)

def createBasicGraph():
    # Initialize a graph
    G = nx.DiGraph()

    # Parse the data and populate the graph with nodes and edges
    for scenario_id, entries in data.items():
        G.add_node(scenario_id, type='scenario')
        for entry in entries:
            image_id = entry['id']  # Use the entry ID as the central node
            G.add_edge(scenario_id, image_id) # always large - small
            G.add_node(image_id, type='image')
            
            for category, value in entry['value'].items():
                # Connect the entry to each category
                G.add_node(category, type='category')
                # G.add_edge(image_id, category)
                
                if isinstance(value, dict):
                    # Handle subcategories
                    for subcategory, subvalue in value.items():
                        # Connect the category to its subcategory
                        G.add_node(subcategory, type='subcategory')
                        G.add_edge(category, subcategory)
                        if isinstance(subvalue, list):
                            # print(subvalue)
                            for item in subvalue:
                                G.add_node(item, type='subsubcategory')
                                G.add_edge(subcategory, item)
                                G.add_edge(image_id, item)
                        else:
                            G.add_node(subvalue, type='subsubcategory')
                            G.add_edge(subcategory, subvalue)
                            G.add_edge(image_id, subvalue)
                        
                        if isinstance(subvalue, list):
                            # For lists, add each item and connect to the subcategory
                            for item in subvalue:
                                G.add_node(item, type='subsubcategory')
                                G.add_edge(subcategory, item)
                                G.add_edge(image_id, item)
                elif isinstance(value, list):
                    # Directly connect category to items in the list
                    for item in value:
                        G.add_node(item, type='subsubcategory')
                        G.add_edge(category, item)
                        G.add_edge(image_id, item)
                else:
                    G.add_node(value, type='subsubcategory')
                    G.add_edge(category, value)
                    G.add_edge(image_id, value)
                    
    # Visualize the graph
    # plt.figure(figsize=(12, 12))
    # pos = nx.spring_layout(G, seed=42)
    # nx.draw(G, pos, with_labels=True, node_size=20, font_size=8)
    # plt.title("Network of Categories and Subcategories")
    # plt.show()
    print("Graph created")
    # nx.write_graphml_lxml(G, "/home/carla/Github/UDrive/Analysis/ArgoVerse1/analysis_directed.graphml")
    return G


def analyasisDegreeCentrality(G, x):
    degree_centrality = nx.degree_centrality(G)
    top_x = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:x]
    for key in top_x:
        print(f"The most {x} common occurances are Key: {key}, Value: {degree_centrality[key]}")  

def calculateJaccardsimilarity(graph1, graph2):
    # Example: Using Jaccard similarity on the edge sets
    nodes1 = set(graph1.nodes())
    nodes2 = set(graph2.nodes())
    # print(nodes1)
    intersection = nodes1.intersection(nodes2)
    union = nodes1.union(nodes2)
    similarity = len(intersection) / len(union)
    return similarity

def calculate_subgraph_density(graph):
    # This function calculates the density for subgraphs centered on each image
    densities = {}
    for node in graph.nodes():
        if graph.nodes[node]['type'] == 'image':
            # Get descendants that form the subgraph for this image
            descendants = nx.descendants(graph, node)
            subgraph = graph.subgraph(descendants.union({node}))
            densities[node] = nx.density(subgraph)
        elif graph.nodes[node]['type'] == 'scenario':
            scenario_name = node
    
    avg_density = sum(densities.values())/len(densities)
    min_density = min(densities.values())
    max_density = max(densities.values())
    range_density = max_density - min_density
    if range_density > 0:
        normalized_densities = {key: (values - min_density) / range_density for key, values in densities.items()}
    else:
        normalized_densities = {key: 0 for key, value in densities.items()}
    scenario_info = {
        'scenario_name': scenario_name,
        'densities': densities,
        'avg_density': avg_density,
        'min_density': min_density,
        'max_density': max_density,
        'normalized_density': normalized_densities
    }
    return scenario_info
        

# ---------------------- Functions that are in Progress ---------------------------

def compareScenarios(G): 
    scenario_subgraph_list = []
    for node, attrs in G.nodes(data=True):
        # print(node[0])
        if attrs.get('type') == "scenario":
            reachable_from_node = nx.descendants(G, node)
            reachable_from_node.add(node)
            subgraph = G.subgraph(reachable_from_node)
            scenario_subgraph_list.append(subgraph)    
            # nx.write_graphml_lxml(subgraph, f"/home/carla/Github/UDrive/Analysis/ArgoVerse1/scenario_subgraphs/subgraph_directed{node}.graphml")
    
    scenario_data = []
    for scenario in scenario_subgraph_list:
        scenario_info = calculate_subgraph_density(scenario)
        scenario_data.append(scenario_info)
    
    with open('/home/carla/Github/UDrive/Analysis/ArgoVerse1/results/scenario_densities.csv', 'w', newline='') as csvfile:
        fieldnames = ['scenario_name', 'densities', 'avg_density', 'min_density','max_density', 'normalized_density']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in scenario_data:
            # Flatten the 'densities' dictionary into a string to fit in a single CSV cell
            data['densities'] = ', '.join(f"{k}:{v}" for k, v in data['densities'].items())
            # print(data)
            writer.writerow(data)
    

  

def compareImages(G): 
    image_subgraph_list = []
    image_names = []
    image_count = 0
    connection_count = 0
    for node, attrs in G.nodes(data=True):
        if attrs.get('type') == "image":
            image_names.append(node)
            direct_descendants = {node}
            image_count += 1     
            # # Add direct children (assuming direct connections to categories/subcategories)
            for successor in G.successors(node):  # Directly connected nodes
                direct_descendants.add(successor)
                connection_count += 1
            #     # If you also want subcategories directly connected to categories:
            #     for sub_successor in G.successors(successor):
            #         direct_descendants.add(sub_successor)
            
            # # Now create and save the subgraph for the image and its direct descendants
            subgraph = G.subgraph(direct_descendants)
            image_subgraph_list.append(subgraph)    
            # nx.write_graphml_lxml(subgraph, f"/home/carla/Github/UDrive/Analysis/ArgoVerse1/image_subgraphs/subgraph_directed{node}.graphml")
    image_average_degree = connection_count/image_count - 1
    print(f"Average degree of image node is {image_average_degree}")
    n = len(image_subgraph_list)
    similarity_matrix = [[0] * (n + 1) for _ in range(n + 1)]

    # Set the first row and first column to image names
    similarity_matrix[0] = [''] + image_names  # First row, starting with an empty string for the top-left cell
    for i in range(1, n + 1):
        similarity_matrix[i][0] = image_names[i - 1] 

    # Calculate similarities
    for i in range(n):
        for j in range(i+1, n):
            sim = calculateJaccardsimilarity(image_subgraph_list[i], image_subgraph_list[j])
            similarity_matrix[i+1][j+1] = sim
            similarity_matrix[j+1][i+1] = sim
        similarity_matrix[i + 1][i + 1] = 1


    with open('imageJaccardSimilaritymatrix.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(similarity_matrix)


def analyzeCombinations(G):
    category_combinations = {}
    for node, data in G.nodes(data=True):
        if data['type'] == 'image':
            categories = [n for n in nx.descendants(G, node) if G.nodes[n]['type'] == 'category']
            print(categories)
            for size in range(2, len(categories)+1):
                for comb in combinations(categories, size):
                    comb = tuple(sorted(comb))
                    if comb not in category_combinations:
                        category_combinations[comb] = 0
                    category_combinations[comb] += 1
    return category_combinations

def predictMissingCombinations(observed_combinations):
    # Placeholder for predicting missing combinations based on observed
    # This could involve comparing with a model or expected patterns
    # For simplicity, here we might look for combinations that are below a certain frequency threshold
    missing_combinations = {comb: count for comb, count in observed_combinations.items() if count < 3}  # Example threshold
    return missing_combinations

G = createBasicGraph()
# compareScenarios(G)
# compareImages(G)
# analyasisDegreeCentrality(G, 20)


category_combinations = analyzeCombinations(G)
missing_combinations = predictMissingCombinations(category_combinations)
print(missing_combinations)







