# Let's start by creating the UML diagrams for the required tasks. First, we'll create a component diagram
# and then a deployment diagram for the Pet Shop Management System.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# Component Diagram

# Create a directed graph
G = nx.DiGraph()

# Adding components (nodes)
components = {
    "Pet Management": {"provides": [], "requires": ["Order Processing", "Product Management"]},
    "Customer Management": {"provides": [], "requires": ["Order Processing"]},
    "Order Processing": {"provides": ["Pet Management", "Product Management"], "requires": ["Supplier Management"]},
    "Product Management": {"provides": ["Order Processing"], "requires": ["Supplier Management"]},
    "Service Management": {"provides": [], "requires": ["Customer Management"]},
    "Supplier Management": {"provides": ["Product Management"], "requires": []},
    "Reporting": {"provides": [], "requires": ["Order Processing", "Product Management", "Customer Management"]},
}

# Add nodes and edges based on component requirements and provides
for component, interfaces in components.items():
    G.add_node(component)
    for provided in interfaces["provides"]:
        G.add_edge(provided, component, label="provides")
    for required in interfaces["requires"]:
        G.add_edge(component, required, label="requires")

# Set positions for a circular layout
pos = nx.circular_layout(G)

# Drawing the graph
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)

# Draw edges with labels
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title("Component Diagram for Pet Shop Management System")
plt.show()


