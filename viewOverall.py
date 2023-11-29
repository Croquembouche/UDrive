import json
import networkx as nx
import matplotlib.pyplot as plt

# Load your JSON data containing category and subcategory structure
with open('WaymoRoadOverallList.json', 'r') as json_file:
    category_structure = json.load(json_file)

# Create a directed graph
G = nx.DiGraph()

# Helper function to recursively add nodes and edges to the graph
def add_nodes_and_edges(category_data, parent_node=None):
    for category, subcategories in category_data.items():
        if parent_node is not None:
            G.add_edge(parent_node, category)
        G.add_node(category)
        if isinstance(subcategories, list):
            for subcategory in subcategories:
                G.add_node(subcategory)
                G.add_edge(category, subcategory)
        elif isinstance(subcategories, dict):
            add_nodes_and_edges(subcategories, category)

# Start the recursive process
add_nodes_and_edges(category_structure)

# Create hierarchical layout positions for categories and subcategories
pos = {}
level_spacing = 1.5
x = 0
y = 0

def create_layout(category_data, parent_x=0, parent_y=0):
    for category, subcategories in category_data.items():
        pos[category] = (parent_x, parent_y)
        y = parent_y
        y -= level_spacing
        if isinstance(subcategories, dict):
            create_layout(subcategories, parent_x + 1, y)
        elif isinstance(subcategories, list):
            for subcategory in subcategories:
                pos[subcategory] = (parent_x + 1, y)
                y -= level_spacing

create_layout(category_structure)

# Draw the graph with the hierarchical layout
plt.figure(figsize=(16, 16))
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=10, alpha=0.7)
plt.title("Categories and Subcategories")
plt.show()
