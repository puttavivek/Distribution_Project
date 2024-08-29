import osmnx as ox
import geopandas as gpd

# Step 1: Download the road network for a specific area (e.g., Downtown Halifax)
place_name = 'South End, Halifax, Nova Scotia, Canada'
G = ox.graph_from_place(place_name, network_type='drive')

# Step 2: Extract edges data from the graph
_, edges = ox.graph_to_gdfs(G)

# Step 3: Plot the road network on an interactive map using GeoPandas explore
map_explorer = edges.explore(color='blue', tooltip='name')

# Step 4: Save the interactive map as an HTML file
map_save_path = "C:/Users/putta/OneDrive - Dalhousie University/Distribution Management/Projects/Data/SouthEnd_map.html"
map_explorer.save(map_save_path)
