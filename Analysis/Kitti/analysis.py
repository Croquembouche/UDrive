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
from scipy.stats import truncnorm
import random
import pandas as pd



# Load your data
file_path = '/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/unifiedAnalysis.json'  # Update this with the actual file path
with open(file_path, 'r') as file:
    data = json.load(file)


class DatasetAnalysis:

    def exportToCSV(self):
        G = self.G
        # Export nodes to CSV for Gephi
        nodes_df = pd.DataFrame(G.nodes(data=True), columns=['Id', 'Label'])
        nodes_df['Label'] = nodes_df['Label'].apply(lambda x: x.get('label', ''))  # Extract label if it exists

        # Ensure there are no empty labels or ids
        nodes_df['Id'] = nodes_df['Id'].astype(str)  # Convert IDs to string if necessary
        nodes_df = nodes_df[nodes_df['Label'].str.strip() != '']  # Remove rows with empty labels
        nodes_df.to_csv('nodes.csv', index=False)

        # Export edges to CSV for Gephi
        edges_df = pd.DataFrame(G.edges(), columns=['Source', 'Target'])
        edges_df['Source'] = edges_df['Source'].astype(str)  # Convert Source to string
        edges_df['Target'] = edges_df['Target'].astype(str)  # Convert Target to string
        edges_df.to_csv('edges.csv', index=False)
    
    def createBasicGraph(self):
        # Initialize a graph
        G = nx.DiGraph()
        subsubcategories = []
        low = 0
        medium = 0
        high = 0
        # Parse the data and populate the graph with nodes and edges
        for image_id, entries in data.items():
            try:
                G.add_node(image_id, type='image')
                for category, value in entries.items():
                    # Connect the entry to each category
                    G.add_node(category, type='category')
                    # G.add_edge(image_id, category)
                    if category == "Severity":
                        if 1 <= value and value <= 3: 
                            low += 1
                        elif 3 <= value and value <= 6: 
                            medium += 1
                        elif 7 <= value and value <= 10: 
                            high += 1
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
                                    if item not in subsubcategories:
                                        subsubcategories.append(item)
                            else:
                                G.add_node(subvalue, type='subsubcategory')
                                G.add_edge(subcategory, subvalue)
                                G.add_edge(image_id, subvalue)
                                if subvalue not in subsubcategories:
                                        subsubcategories.append(subvalue)
                            
                            if isinstance(subvalue, list):
                                # For lists, add each item and connect to the subcategory
                                for item in subvalue:
                                    G.add_node(item, type='subsubcategory')
                                    G.add_edge(subcategory, item)
                                    G.add_edge(image_id, item)
                                    if item not in subsubcategories:
                                        subsubcategories.append(item)
                    elif isinstance(value, list):
                        # Directly connect category to items in the list
                        for item in value:
                            G.add_node(item, type='subsubcategory')
                            G.add_edge(category, item)
                            G.add_edge(image_id, item)
                            if item not in subsubcategories:
                                subsubcategories.append(item)
                    else:
                    
                        G.add_node(value, type='subsubcategory')
                        G.add_edge(category, value)
                        G.add_edge(image_id, value)
                        if value not in subsubcategories:
                            subsubcategories.append(value)
            except:
                print(image_id)
                        
        # Visualize the graph
        # plt.figure(figsize=(12, 12))
        # pos = nx.spring_layout(G, seed=42)
        # nx.draw(G, pos, with_labels=True, node_size=20, font_size=8)
        # plt.title("Network of Categories and Subcategories")
        # plt.show()
        print("Graph created")
        # num_edges = G.number_of_edges()
        # num_nodes = G.number_of_nodes()
        self.G = G
        print(subsubcategories)
        print(f"{len(subsubcategories)} number of subsubcategories")
        print(f"The dataset contains {low} low-risk scenes, {medium} medium-risk scenes, and {high} high-risk scenes.")
        # print(f"Number of Edges: {num_edges}")
        # print(f"Number of Edges: {num_nodes}")
        # Export to GEXF
        # nx.write_gexf(G, "/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/analysis_directed.gexf")
        nx.write_graphml_lxml(G, "/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/analysis_directed.graphml")
        # self.exportToCSV()
        return G


    def calculateDegreeCentrality(self, x):
        degree_centrality = nx.degree_centrality(self.G)
        top_x = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:x]
        values = list(degree_centrality.values())
        values_array = np.array(values)
        print(f"Degree Centrality: mean:{np.mean(values_array)}, max:{np.max(values_array)}, min:{np.min(values_array)}, std:{np.std(values_array)}")
        for key in top_x:
            print(f"The most {x} common occurances are Key: {key}, Value: {degree_centrality[key]}")  


    def calculateBetweennessCentrality(self):
        # Calculate betweenness centrality for all nodes
        centrality = nx.betweenness_centrality(self.G)
        
        values = list(centrality.values())

        # Calculate the 95th percentile as the threshold
        threshold = np.percentile(values, 95)

        # Identify nodes with high betweenness centrality above the 95th percentile
        high_centrality_nodes = [node for node, cent in centrality.items() if cent >= threshold and ".jpg" not in node]

        print(f"High Centrality Nodes: {high_centrality_nodes}")


    def calculateJaccardsimilarity(self, graph1, graph2):
        # Example: Using Jaccard similarity on the edge sets
        nodes1 = set(graph1.nodes())
        nodes2 = set(graph2.nodes())
        # print(nodes1)
        # print(nodes2)
        intersection = nodes1.intersection(nodes2)
        # print(intersection)
        union = nodes1.union(nodes2)
        # print(union)
        similarity = len(intersection) / len(union)
        # print(similarity)
        return similarity

    def calculate_subgraph_density(self, graph):
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


    def calculateImageNodeDistribution(self, image_subgraph_list):
        image_subgraph_num_node = []
        for subgraph in image_subgraph_list:
            image_subgraph_num_node.append(subgraph.number_of_nodes()-1) # -1 to remove the root node
        print(f"Number of images: {len(image_subgraph_list)}")
        print(f"min_value: {np.min(image_subgraph_num_node)}, max_value: {np.max(image_subgraph_num_node)}, average_value: {np.mean(image_subgraph_num_node)}, std: {np.std(image_subgraph_num_node)}")

    def get_truncated_normal(self, mean=0, sd=1, low=0, upp=10):
        """Return a sample from a truncated normal distribution"""
        return truncnorm(
            (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


    def matrixAnalysis(self, matrix):
        mask = matrix != 1.0
        filtered_matrix = matrix[mask]
        # Calculate mean ignoring 1s
        mean_value = np.mean(filtered_matrix)
        # Calculate minimum ignoring 1s
        min_value = np.min(filtered_matrix)
        # Calculate maximum ignoring 1s
        max_value = np.max(filtered_matrix)
        print(f"Mean: {mean_value}, Min: {min_value}, Max: {max_value}, STD: {np.std(filtered_matrix)}")

    def createRandomImageGraph(self, root_node):
        NUM_NODES = 311  # Includes the root node
        MEAN_CONNECTIONS = 22.385847797062752
        STD_DEV_CONNECTIONS = 2.4488055960668373
        MIN_CONNECTIONS = 7

        graph = nx.DiGraph()
        # Add nodes (node 0 is the root node)
        graph.add_nodes_from(range(NUM_NODES))

        # Define root and special categories nodes
        special_categories = {
            'scene_node': random.randint(1, 12),
            'timeofday_node': random.randint(13, 15),
            'weather_node': random.randint(16, 22),
            'roadcondition_node': random.randint(23, 24),
            'numlane_node': random.randint(25, 31),
            'lanemarking_node': random.randint(32, 34),
            'trafvis_node': random.randint(130, 132),
            'trafstate_node': random.randint(133, 138),
            'vehiclenum_node': random.randint(139, 142),
            'vehiclemotion_node': range(143, 144),
            'police_node_present':random.randint(221, 222),
            'police_node_state':random.randint(223, 224),
            'bicycle_node_present':random.randint(225, 226),
            'bicycle_node_state':random.randint(227, 231),
            'animal_node_present':random.randint(232, 233),
            'animal_node_state':random.randint(234, 236),
            'direction_node': random.randint(237, 242),
            'egodirection_node': random.randint(243, 255),
            'egomanu_node': random.randint(256, 282),
            'vis_node': random.randint(283, 286),
            'cam_node': random.randint(294, 299),
            'sev_node': random.randint(300, 309),
        }

        # Nodes to choose multiple from and their potential ranges
        multiple_connection_categories = {
            'speciallane_node': range(34, 51),
            'trafficsign_node': range(50, 129),
            'vehicletype_node': range(145, 182),
            'vehiclestate_node': range(183, 211),
            'ped_node': range(212, 220),
            'impair_node': range(287, 293),
        }

        # Add edges from root node to special categories nodes
        for node in special_categories.values():
            graph.add_edge(root_node, node)
        

        # Adjust total number of connections from the root, including the special categories
        additional_connections_needed = max(MIN_CONNECTIONS, int(random.gauss(MEAN_CONNECTIONS, STD_DEV_CONNECTIONS))) - len(special_categories)
        additional_connections_needed = max(0, additional_connections_needed)  # Ensure no negative number
        potential_child_nodes = [n for n in range(1, NUM_NODES) if n not in special_categories.values()]

        # Randomly choose additional nodes to connect from the root, avoiding duplicates
        additional_child_nodes = random.sample(potential_child_nodes, min(additional_connections_needed, len(potential_child_nodes)))

        # Connect these additional nodes to the root
        for node in additional_child_nodes:
            graph.add_edge(root_node, node)

        # Remove unconnected nodes
        unconnected_nodes = [node for node in graph.nodes if graph.degree(node) == 0]
        graph.remove_nodes_from(unconnected_nodes)
        
        return graph
    
    def randomAnalysis(self, similarity_threshold=0.9):
        random_image_graph = []
        for i in range(749):
            temp = self.createRandomImageGraph(root_node=i+10000)
            random_image_graph.append(temp)
            nx.write_graphml_lxml(temp, f"/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/random_graphs/random_subgraph_directed-{i}.graphml")
        self.random_image_graph = random_image_graph
        n = len(random_image_graph)
        similarity_matrix = similarity_matrix = np.zeros((n, n), dtype=object)
        for i in range(0,n):
            for j in range(i, n):
                sim = self.calculateJaccardsimilarity(random_image_graph[i], random_image_graph[j])
                similarity_matrix[i][j] = sim
                similarity_matrix[j][i] = sim
            similarity_matrix[i][i] = 1
        self.matrixAnalysis(similarity_matrix)

        for vary in range(10, -1, -1):
            value = vary/10
            to_remove = set()
            similar_count = 0
            for i in range(0, n):
                for j in range(0, n):
                    if i != j and similarity_matrix[i][j] > value:
                        to_remove.add(i)
                        similar_count+=1
            print(f"Random dataset: Found {similar_count//2} pairs of similar scenes with threshold at {value}")
        
        # do it again for threshold = 0.5
        # similarity_threshold = 0.4
        # similarity_matrix = similarity_matrix = np.zeros((n, n), dtype=object)
        # for i in range(0,n):
        #     for j in range(i, n):
        #         sim = self.calculateJaccardsimilarity(random_image_graph[i], random_image_graph[j])
        #         similarity_matrix[i][j] = sim
        #         similarity_matrix[j][i] = sim
        #     similarity_matrix[i][i] = 1
        # self.matrixAnalysis(similarity_matrix)
        # to_remove = set()
        # similar_count = 0
        # for i in range(0, n):
        #     for j in range(0, n):
        #         if i != j and similarity_matrix[i][j] > similarity_threshold:
        #             to_remove.add(i)
        #             similar_count+=1
        # print(f"Found {similar_count//2} pairs of similar scenes with threshold at {similarity_threshold}")

    def checkScenario(self, image1, image2):
        im1_parent = ""
        im2_parent = ""
        
        found1 = False
        found2 = False
        while found1 == False and found2 == False:
            for scenario in self.scenario_subgraph_list:
                for node, attrs in scenario.nodes(data=True):   
                    if attrs.get('type') == "image" and node == image1:
                        im1_parent = [source for source, dest in scenario.edges() if dest == node][0]
                        found1 = True
                    if attrs.get('type') == "image" and node == image2:
                        im2_parent = [source for source, dest in scenario.edges() if dest == node][0]
                        found2 = True
        # print(im1_parent, im2_parent)
        if im1_parent == im2_parent:
            return 1
        else:
            return 0




    # ---------------------- Functions that are in Progress ---------------------------

    # def compareScenarios(self): 
    #     scenario_subgraph_list = []
    #     for node, attrs in self.G.nodes(data=True):
    #         # print(node[0])
    #         if attrs.get('type') == "scenario":
    #             reachable_from_node = nx.descendants(self.G, node)
    #             reachable_from_node.add(node)
    #             subgraph = self.G.subgraph(reachable_from_node)
    #             scenario_subgraph_list.append(subgraph)    
    #             # nx.write_graphml_lxml(subgraph, f"/home/carla/Github/UDrive/Analysis/ArgoVerse1/scenario_subgraphs/subgraph_directed{node}.graphml")
    #     # self.calculateBetweennessCentrality()
    #     scenario_data = []
    #     for scenario in scenario_subgraph_list:
    #         scenario_info = self.calculate_subgraph_density(scenario)
    #         scenario_data.append(scenario_info)
    #     self.scenario_subgraph_list = scenario_subgraph_list
    #     print(f"Total {len(scenario_subgraph_list)} scenarios")
    #     with open('/home/carla/Github/UDrive/Analysis/ArgoVerse1/results/scenario_densities.csv', 'w', newline='') as csvfile:
    #         fieldnames = ['scenario_name', 'densities', 'avg_density', 'min_density','max_density', 'normalized_density']
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
    #         writer.writeheader()
    #         for data in scenario_data:
    #             # Flatten the 'densities' dictionary into a string to fit in a single CSV cell
    #             data['densities'] = ', '.join(f"{k}:{v}" for k, v in data['densities'].items())
    #             # print(data)
    #             writer.writerow(data)
        

    def compareImages(self, similarity_threshold=1.0): 
        image_subgraph_list = []
        image_names = []
        image_count = 0
        connection_count = 0
        for node, attrs in self.G.nodes(data=True):
            if attrs.get('type') == "image":
                image_names.append(node)
                direct_descendants = {node}
                image_count += 1
                    
                # # Add direct children (assuming direct connections to categories/subcategories)
                for successor in self.G.successors(node):  # Directly connected nodes
                    direct_descendants.add(successor)
                    connection_count += 1
                #     # If you also want subcategories directly connected to categories:
                #     for sub_successor in G.successors(successor):
                #         direct_descendants.add(sub_successor)
                
                # # Now create and save the subgraph for the image and its direct descendants
                subgraph = self.G.subgraph(direct_descendants)
                image_subgraph_list.append(subgraph)   
                nx.write_graphml_lxml(subgraph, f"/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/image_subgraph/subgraph_directed{node}.graphml")
        self.calculateImageNodeDistribution(image_subgraph_list)
        n = len(image_subgraph_list)
        similarity_matrix = np.zeros((n + 1, n + 1), dtype=object)
        
        # Set the first row and first column to image names
        similarity_matrix[0] = [''] + image_names  # First row, starting with an empty string for the top-left cell
        for i in range(1, n + 1):
            similarity_matrix[i][0] = image_names[i - 1] 

        # Calculate similarities
        for i in range(n):
            for j in range(i+1, n):
                sim = self.calculateJaccardsimilarity(image_subgraph_list[i], image_subgraph_list[j])
                similarity_matrix[i+1][j+1] = sim
                similarity_matrix[j+1][i+1] = sim
            similarity_matrix[i + 1][i + 1] = 1
        self.matrixAnalysis(similarity_matrix[1:, 1:] )
        
        # with open('/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/results/imageJaccardSimilaritymatrix.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(similarity_matrix)

        # Filter images based on similarity threshold
        
        for vary in range(10, -1, -1):
            value = vary/10
            similar_count = 0
            to_remove = set()
            for i in range(1, n+1):
                for j in range(1, n+1):
                    if i != j and similarity_matrix[i][j] > value:
                        to_remove.add(i)
                        similar_count+=1
            print(f"Found {similar_count//2} number of similar scenes with threshold at {value}.")
        similar_count = 0
        to_remove = set()
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i != j and similarity_matrix[i][j] > similarity_threshold:
                    to_remove.add(i)
                    similar_count+=1
        print(f"Found {similar_count//2} number of similar scenes with threshold at {similarity_threshold}.")

        # Writing to CSV while skipping filtered out graphs
        filtered_similarity_matrix = [row for index, row in enumerate(similarity_matrix) if index not in to_remove]
        filtered_image_names = [name for index, name in enumerate(image_names) if index not in to_remove]

        # with open('/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/results/filtered_imageJaccardSimilaritymatrix.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([''] + filtered_image_names)
        #     for name, row in zip(filtered_image_names, filtered_similarity_matrix):
        #         try:
        #             writer.writerow([name] + row)
        #         except:
        #             pass
    

    def createRandomDataset(self):
        random_dataset = nx.DiGraph()
        # scenario_nodes = ['scenario_' + str(i) for i in range(65)]
        # random_dataset.add_nodes_from(scenario_nodes)
        for subgraph in self.random_image_graph:
            for node in subgraph.nodes():
                random_dataset.add_node(node)
            
            for edge in subgraph.edges():
                u,v = edge
                random_dataset.add_edge(u, v)
        degree_centrality = nx.degree_centrality(random_dataset)
        # top_x = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:x]
        values = list(degree_centrality.values())
        values_array = np.array(values)
        print(f"Random Graph Degree Centrality: mean:{np.mean(values_array)}, max:{np.max(values_array)}, min:{np.min(values_array)}, std:{np.std(values_array)}")
        nx.write_graphml_lxml(random_dataset, f"/media/william/blueicedrive/Github/UDrive/Analysis/Kitti/randomdataset.graphml")
    
    def calculateCompositeScore(self):
        w1 = 0.4
        w2 = 0.2
        w3 = 0.2
        w4 = 0.1
        w5 = 0.2
        high_risk = 6
        medium_risk = 135
        low_risk = 599
        c_max = 0.7545271629778673
        c_sigma = 0.07712440833368164
        c_max_random = 0.718809980806142
        c_random_sigma = 0.05188612479739662
        density = 0.017
        density_random = 0.016
        modularity = 0.133
        modulartiy_random = 0.078
        num_community = 42
        num_community_random = 50
        J_image = 0.34552989945838775
        J_random = 0.16649884620645025
        J_penalty = (J_image - J_random)/J_random
        M_penalty = ((modularity - modulartiy_random)/modulartiy_random) * ((num_community-num_community_random)/num_community_random)
        C_penalty = (c_max - c_max_random)/c_max_random + (c_sigma-c_random_sigma)/c_random_sigma
        D_penalty = (density - density_random)/density_random
        
        mean = (high_risk + medium_risk + low_risk) / 3
        D_H = abs(high_risk - mean)
        D_M = abs(medium_risk - mean)
        D_L = abs(low_risk - mean)      
        RD_penalty = (D_H + D_M + D_L)/mean/10
        S = 1-(w1*J_penalty - w2*M_penalty + w3*C_penalty + w4*D_penalty)-w5*RD_penalty
        print(f"The Composite Score of Kitti is {S}. J_penalty: {w1*J_penalty}, M_penalty: {w2*M_penalty}, C_penalty: {w3*C_penalty}, D_penalty: {w4*D_penalty}, RiskDistribution_penalty: {RD_penalty}")
# The Composite Score of Kitti is 0.35248652763298316.. J_penalty: 0.2525156083924665, M_penalty: -0.18389189189189187 C_penalty: 0.045497857569434426, D_penalty: -0.06842105263157895, RiskDistribution_penalty: 0.1798938287989383

        





G = DatasetAnalysis()
# G.createBasicGraph()
# print("Compare Scenarios")
# G.compareScenarios()
# print("Kitti Results")
# G.compareImages(0.8)
# G.compareImages(0.9)
# G.calculateDegreeCentrality(10)
# print("Random Graph Results")
# G.randomAnalysis()
# G.createRandomDataset()
G.calculateCompositeScore()









