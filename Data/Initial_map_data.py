import osmnx as ox
import pandas as pd
from math import atan2, degrees

# Step 1: Download the road network for a specific area (e.g., Downtown Halifax)
place_name = 'Fairview ,Halifax, Nova Scotia, Canada'
G = ox.graph_from_place(place_name, network_type='drive')

# Step 2: Extract nodes and edges data from the graph
nodes, edges = ox.graph_to_gdfs(G)

# Step 3: Extract 'u' and 'v' (start and end node IDs) directly from the graph edges
# Convert the edges in the graph to a DataFrame
edge_list = []
for u, v, data in G.edges(data=True):
    edge_list.append({
        'u': u,
        'v': v,
        'length': data.get('length', None),  # Length of the edge
        'name': data.get('name', 'Unknown'),  # Street name
        'highway': data.get('highway', 'Unknown'),  # Highway type
        'maxspeed': data.get('maxspeed', None),  # Max speed if available
        'oneway': data.get('oneway', False)  # One-way (True) or two-way (False)
    })

# Convert to DataFrame
edge_df = pd.DataFrame(edge_list)

# Step 4: Use node indices for mapping, since 'osmid' is not available
edge_df['u_x'] = edge_df['u'].map(nodes['x'])
edge_df['u_y'] = edge_df['u'].map(nodes['y'])
edge_df['v_x'] = edge_df['v'].map(nodes['x'])
edge_df['v_y'] = edge_df['v'].map(nodes['y'])

# Step 5: Add direction information for one-way roads (bearing from u to v)
def calculate_bearing(x1, y1, x2, y2):
    # Calculate bearing between two points in degrees
    angle = atan2(y2 - y1, x2 - x1)
    bearing = degrees(angle)
    return (bearing + 360) % 360  # Normalize bearing to [0, 360] degrees

# Add bearing information for one-way roads
edge_df['bearing'] = edge_df.apply(lambda row: calculate_bearing(row['u_x'], row['u_y'], row['v_x'], row['v_y']) if row['oneway'] else None, axis=1)

# Step 6: Define the file path for saving data and images
save_path = "C:/Users/putta/OneDrive - Dalhousie University/Distribution Management/Projects/Data/"

# Step 7: Export nodes and edges to CSV or Excel files

nodes.to_excel(f'{save_path}nodes_fairview.xlsx', index=True)


edge_df.to_excel(f'{save_path}edges_fairview.xlsx', index=False)

# Step 8: Plot the road network graph and save the image
fig, ax = ox.plot_graph(G, show=False, close=False)
fig.savefig(f'{save_path}fairview.png', dpi=300)

# Optional: Print first few rows to check the data
print("Nodes Data:")
print(nodes.head())
print("\nEdges Data:")
print(edge_df.head())
