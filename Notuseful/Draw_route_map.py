import pandas as pd
import folium
import math
import matplotlib.pyplot as plt

# Load the Excel file with the coordinates from the "Nodes" sheet
file_path = r"C:\Users\putta\OneDrive - Dalhousie University\Distribution Management\Projects\Final\Data\springhill_network_data.xlsx"  # Replace with the actual path to your Excel file
df = pd.read_excel(file_path, sheet_name='Nodes')

# Define the route you want to plot
route_1 = [29 ,  30 ,  27 ,  30 ,  32 ,  50 ,  32 ,  52 ,  51 ,  50 ,  48 ,  41 ,  48 ,  45 ,  39 ,  45 ,  40 ,  34 ,
           25 ,  19 ,  25 ,  26 ,  22 ,  16 ,  14 ,  11 ,  10 ,  11 ,  12 ,  11 ,  14 ,  13 ,  14 ,  15 ,  14 ,  16 ,
           18 ,  16 ,  22 ,  21 ,  22 ,  23 ,  22 ,  26 ,  25 ,  34 ,  40 ,  35 ,  40 ,  45 ,  48 ,  50 ,  51 ,  52 ,
           87 ,  86 ,  84 ,  81 ,  51 ,  81 ,  80 ,  81 ,  84 ,  83 ,  56 ,  50 ,  56 ,  54 ,  48 ,  54 ,  56 ,  83 ,
           82 ,  71 ,  54 ,  71 ,  68 ,  45 ,  68 ,  63 ,  40 ,  63 ,  61 ,  53 ,  34 ,  53 ,  49 ,  47 ,  42 ,  47 ,
           44 ,  37 ,  33 ,  26 ,  33 ,  37 ,  36 ,  28 ,  36 ,  31 ,  24 ,  10 ,  24 ,  20 ,  6 ,  7 ,  2 ,  1 ,  2 ,
           4 ,  2 ,  7 ,  8 ,  5 ,  3 ,  4 ,  3 ,  5 ,  4 ,  5 ,  8 ,  9 ,  3 ,  9 ,  8 ,  7 ,  6 ,  20 ,  17 ,  20 ,
           24 ,  31 ,  36 ,  37 ,  44 ,  38 ,  33 ,  38 ,  44 ,  47 ,  46 ,  38 ,  46 ,  43 ,  46 ,  47 ,  49 ,  53 ,
           60 ,  53 ,  61 ,  55 ,  61 ,  63 ,  68 ,  71 ,  82 ,  79 ,  75 ,  66 ,  61 ,  66 ,  73 ,  66 ,  75 ,  68 ,
           75 ,  79 ,  82 ,  83 ,  84 ,  86 ,  87 ,  88 ,  89 ,  70 ,  89 ,  88 ,  104 ,  100 ,  91 ,  100 ,  98 ,  86 ,
           98 ,  97 ,  83 ,  97 ,  96 ,  82 ,  96 ,  97 ,  98 ,  100 ,  104 ,  107 ,  89 ,  90 ,  67 ,  59 ,  67 ,  69 ,
           67 ,  90 ,  89 ,  107 ,  104 ,  120 ,  119 ,  118 ,  100 ,  118 ,  116 ,  98 ,  116 ,  114 ,  97 ,  114 ,
           109 ,  96 ,  109 ,  103 ,  95 ,  79 ,  95 ,  94 ,  85 ,  163 ,  72 ,  64 ,  72 ,  65 ,  62 ,  49 ,  62 ,  58
    ,  44 ,  58 ,  57 ,  58 ,  62 ,  65 ,  76 ,  65 ,  72 ,  163 ,  85 ,  164 ,  73 ,  78 ,  73 ,  164 ,  163 ,  164 ,
           85 ,  94 ,  95 ,  103 ,  109 ,  114 ,  116 ,  118 ,  119 ,  120 ,  121 ,  107 ,  111 ,  90 ,  92 ,  69 ,  74
    ,  69 ,  92 ,  90 ,  111 ,  107 ,  121 ,  122 ,  124 ,  111 ,  113 ,  92 ,  93 ,  74 ,  77 ,  74 ,  93 ,  92 ,  113
    ,  111 ,  124 ,  122 ,  137 ,  131 ,  125 ,  117 ,  112 ,  99 ,  94 ,  99 ,  102 ,  99 ,  112 ,  103 ,  112 ,  117 ,
           125 ,  119 ,  125 ,  131 ,  127 ,  117 ,  127 ,  123 ,  102 ,  101 ,  102 ,  123 ,  110 ,  123 ,  127 ,  131 ,
           137 ,  142 ,  126 ,  124 ,  126 ,  128 ,  115 ,  105 ,  93 ,  105 ,  106 ,  105 ,  115 ,  113 ,  115 ,  128 ,
           126 ,  142 ,  137 ,  148 ,  147 ,  144 ,  140 ,  131 ,  140 ,  136 ,  133 ,  127 ,  133 ,  130 ,  123 ,  130 ,
           133 ,  136 ,  140 ,  144 ,  147 ,  153 ,  147 ,  148 ,  149 ,  129 ,  128 ,  129 ,  132 ,  106 ,  108 ,  106 ,
           132 ,  129 ,  149 ,  142 ,  149 ,  148 ,  157 ,  155 ,  152 ,  139 ,  152 ,  143 ,  134 ,  132 ,  134 ,  146 ,
           134 ,  143 ,  151 ,  143 ,  152 ,  155 ,  157 ,  156 ,  144 ,  156 ,  154 ,  145 ,  135 ,  130 ,  135 ,  138 ,
           133 ,  138 ,  135 ,  145 ,  150 ,  141 ,  136 ,  141 ,  138 ,  141 ,  150 ,  145 ,  154 ,  150 ,  154 ,  156 ,
           158 ,  160 ,  159 ,  160 ,  161 ,  162 ,  161 ,  160 ,  158 ,  156 ,  157 ,  148 ,  137 ,  122 ,  121 ,  120 ,
           104 ,  88 ,  87 ,  52 ,  32 ,  30 ,  29]  # Placeholder data for route 1, replace with actual route data


# Extract the coordinates for each node in the routes
def get_route_coordinates(route, df):
    route_coordinates = []
    for node in route:
        node_data = df[df['UID'] == node]
        if not node_data.empty:
            u_x, u_y = node_data['x'].values[0], node_data['y'].values[0]
            route_coordinates.append([u_y, u_x])
    return route_coordinates


# Get the coordinates for the route
route_1_coordinates = get_route_coordinates(route_1, df)

# Create a folium map centered on the first coordinate of the route
m = folium.Map(location=route_1_coordinates[0], zoom_start=14)

# Add the route (Route 1) in blue
folium.PolyLine(route_1_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)


# Function to add arrows as markers along the route
def add_arrows(map_obj, route_coords, n_arrows=5, color="blue"):
    for i in range(len(route_coords) - 1):
        start = route_coords[i]
        end = route_coords[i + 1]

        # Calculate direction vectors and distances
        dx = end[1] - start[1]
        dy = end[0] - start[0]
        dist = math.sqrt(dx ** 2 + dy ** 2)

        # Add intermediate arrow points
        for j in range(1, n_arrows + 1):
            factor = j / (n_arrows + 1)
            mid_x = start[1] + factor * dx
            mid_y = start[0] + factor * dy

            folium.RegularPolygonMarker(
                location=[mid_y, mid_x],
                fill_color=color,
                number_of_sides=3,
                radius=5,
                rotation=math.degrees(math.atan2(dy, dx)) + 90,
            ).add_to(map_obj)


# Add arrows to the route (blue arrows)
add_arrows(m, route_1_coordinates, color="blue")

# Highlight the starting and ending nodes of the route
# Start (green), end (orange)
folium.Marker(location=route_1_coordinates[0], popup="Route Start", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=route_1_coordinates[-1], popup="Route End", icon=folium.Icon(color='orange')).add_to(m)

# Save the map as an HTML file
m.save("route_map.html")

# Plot the route with arrows using Matplotlib
plt.figure(figsize=(10, 7))  # Adjust the size of the plot

for i in range(len(route_1_coordinates) - 1):
    start = route_1_coordinates[i]
    end = route_1_coordinates[i + 1]

    plt.arrow(start[1], start[0], end[1] - start[1], end[0] - start[0],
              color='blue', head_width=0.0005, head_length=0.0005,  # Increase head width and length for visibility
              linewidth=0.5, length_includes_head=True)  # Reduce line width for thinner lines

# Mark start and end points
plt.scatter(route_1_coordinates[0][1], route_1_coordinates[0][0], color='green', s=100, label='Start Node')
plt.scatter(route_1_coordinates[-1][1], route_1_coordinates[-1][0], color='orange', s=100, label='End Node')

plt.xlabel('Longitude (u_x, v_x)')
plt.ylabel('Latitude (u_y, v_y)')
plt.title('Route Plot')
plt.legend()

# Show plot
plt.show()
