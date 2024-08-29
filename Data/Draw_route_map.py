import pandas as pd
import folium
import math

# Load the Excel file with the coordinates
file_path = r"C:\Users\putta\OneDrive - Dalhousie University\Distribution Management\Projects\Data\X\southendedges.xlsx"  # Replace with the actual path to your Excel file
df = pd.read_excel(file_path)

# Define two routes you want to plot
route_1 = [37, 34, 16, 59, 9, 14, 10, 39, 11, 39, 10, 14, 9, 59, 64, 5, 64, 35, 69, 35, 64, 59, 16, 67, 53, 47, 22, 15,
           40, 15, 60, 30, 54, 7, 71, 40, 33, 40, 71, 7, 54, 30, 62, 29, 22, 47, 45, 44, 45, 48, 45, 47, 53, 67, 16, 34,
           49, 34, 37]
route_2 = [73, 26, 61, 42, 61, 26, 73]


# Extract the coordinates for each node in the routes
def get_route_coordinates(route, df):
    route_coordinates = []
    for node in route:
        node_data = df[(df['UID'] == node) | (df['VID'] == node)]
        if not node_data.empty:
            if node_data['UID'].values[0] == node:
                u_x, u_y = node_data['u_x'].values[0], node_data['u_y'].values[0]
            else:
                u_x, u_y = node_data['v_x'].values[0], node_data['v_y'].values[0]
            route_coordinates.append([u_y, u_x])
    return route_coordinates


# Get the coordinates for each route
route_1_coordinates = get_route_coordinates(route_1, df)
route_2_coordinates = get_route_coordinates(route_2, df)

# Create a folium map centered on the first coordinate of the first route
m = folium.Map(location=route_1_coordinates[0], zoom_start=14)

# Add the first route (Route 1) in blue
folium.PolyLine(route_1_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

# Add the second route (Route 2) in red
folium.PolyLine(route_2_coordinates, color="red", weight=2.5, opacity=1).add_to(m)


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


# Add arrows to the first route (blue arrows)
add_arrows(m, route_1_coordinates, color="blue")

# Add arrows to the second route (red arrows)
add_arrows(m, route_2_coordinates, color="red")

# Highlight the starting and ending nodes of each route
# Route 1 (blue): start (green), end (orange)
folium.Marker(location=route_1_coordinates[0], popup="Route 1 Start", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=route_1_coordinates[-1], popup="Route 1 End", icon=folium.Icon(color='orange')).add_to(m)

# Route 2 (red): start (green), end (orange)
folium.Marker(location=route_2_coordinates[0], popup="Route 2 Start", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=route_2_coordinates[-1], popup="Route 2 End", icon=folium.Icon(color='orange')).add_to(m)

# Save the map as an HTML file
m.save("route_map_with_two_routes.html")
