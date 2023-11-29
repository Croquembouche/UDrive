import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# Load your JSON data
with open('WaymoRoadJson.json', 'r') as json_file:
    data = json.load(json_file)

# Create a directed graph
G = nx.DiGraph()

# Helper function to recursively add nodes and edges to the graph
def add_nodes_and_edges(data, parent_node=None):
    for key, value in data.items():
        if parent_node is not None:
            G.add_edge(parent_node, key)
        if isinstance(value, dict):
            add_nodes_and_edges(value, key)
        elif isinstance(value, list):
            for item in value:
                G.add_node(item)
                G.add_edge(key, item)
        else:
            G.add_node(value)
            G.add_edge(key, value)

# Start the recursive process
add_nodes_and_edges(data)

# Use Fruchterman-Reingold layout with adjusted parameters
pos = nx.spring_layout(G, seed=42, k=0.2, iterations=50, scale=10)

# Draw the graph with a more spread-out layout
plt.figure(figsize=(120, 120))
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, alpha=0.7)
plt.title("Scene Categories and Subcategories")
plt.show()
