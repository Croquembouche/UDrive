import json
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

    

# The 'Scene' key contains a list, so let's adjust our approach to handle lists at the first level of the hierarchy.
# We'll define a new function to handle the addition of nodes and edges considering this structure.

def add_nodes_edges_from_list(graph, parent, child_list):
    # Each item in the list is considered a subcategory or an item itself
    for item in child_list:
        # Create a unique node identifier for each item
        node_name = f"{parent}_{item}"
        graph.add_node(node_name, label=item)
        graph.add_edge(parent, node_name)

    
def visualizeAnalysis():
    print("")


def loadFileandVisualize():
    # Load the JSON data from the file
    file_path = '/home/carla/Github/UDrive/WaymoRoadOverall.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Reinitialize the directed graph
    G = nx.DiGraph()

    # Reuse the previously defined function to add nodes and edges to the graph
    for category, items in data.items():
        G.add_node(category, label=category)
        if isinstance(items, list):
            add_nodes_edges_from_list(G, category, items)

    # Use the Graphviz 'dot' layout
    pos = graphviz_layout(G, prog='dot')

    # Calculate node sizes based on degree to improve readability
    node_sizes = [G.degree(node) * 10 for node in G.nodes()]

    # Draw the graph using the 'dot' layout
    plt.figure(figsize=(30, 30))  # Increase figure size
    smaller_font_size = 8  # Reduce font size to prevent overlap
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'),
            node_size=node_sizes, node_color="skyblue", font_size=10, font_weight="bold",
            arrows=True, arrowstyle="-|>", arrowsize=10)

    # Save the plot to a file
    dot_layout_graph_image_path = '/home/carla/Github/UDrive/dot_layout_network_graph.png'
    plt.savefig(dot_layout_graph_image_path, format='PNG')
    plt.close()  # Close the plot to avoid displaying in this environment