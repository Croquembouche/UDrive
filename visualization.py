import json
import networkx as nx
import matplotlib.pyplot as plt

# Load JSON data
with open('/home/carla/Github/UDrive/WaymoRoadOverall.json', 'r') as file:
    data = json.load(file)

# Create a directed graph
G = nx.DiGraph()

# Iterate over categories in the JSON, adding nodes and edges
for category, items in data.items():
    G.add_node(category)  # Add main category node
    if isinstance(items, list):
        for item in items:
            G.add_node(item)
            G.add_edge(category, item)  # Connect main category to subcategory
    elif isinstance(items, dict):
        for subcategory, subitems in items.items():
            subcategory_full_name = f"{category} - {subcategory}"
            G.add_node(subcategory_full_name)
            G.add_edge(category, subcategory_full_name)  # Connect category to subcategory
            if isinstance(subitems, list):
                for item in subitems:
                    G.add_node(item)
                    G.add_edge(subcategory_full_name, item)  # Connect subcategory to item

# Draw the graph
plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
plt.show()
