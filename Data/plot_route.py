from collections import defaultdict
import pandas as pd
import folium
import math
import matplotlib.pyplot as plt

# Function to read routes from a file
def read_routes_from_file(file_path):
    routes = defaultdict(list)
    distances = {}  # Store distances between nodes
    with open(file_path, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            if line.strip():  # Skip empty lines
                i, j, xijv1 = map(int, line.split())
                # Add each route and repeat it for `xijv1` times
                for _ in range(xijv1):
                    routes[i].append(j)
                # Store the distance for this route
                distances[(i, j)] = xijv1
    return routes, distances

# Function to find all routes using DFS
def find_all_routes(routes, start_node, distances):
    stack = [start_node]
    route = []
    total_distance = 0  # Initialize total distance

    # Traverse the graph
    while stack:
        current_node = stack[-1]

        # If there are routes from the current node
        if routes[current_node]:
            # Get the next destination and move there
            next_node = routes[current_node].pop(0)
            stack.append(next_node)
            # Add distance for the current route
            total_distance += distances.get((current_node, next_node), 1)  # Assuming distance is 1 if not specified
        else:
            # If no more routes from current_node, add to final route
            route.append(stack.pop())

    return route[::-1], total_distance  # Reverse the list to get the route in the right order

# Function to get route coordinates from the DataFrame
def get_route_coordinates(route, df):
    route_coordinates = []
    for node in route:
        node_data = df[df['UID'] == node]
        if not node_data.empty:
            u_x, u_y = node_data['x'].values[0], node_data['y'].values[0]
            route_coordinates.append([u_y, u_x])
    return route_coordinates

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

# Load routes from the text file
file_path = r"AMPLoutput.txt"  # Replace with actual path
routes, distances = read_routes_from_file(file_path)

# Specify the starting node
start_node = int(input("Enter the starting node: "))

# Generate the route and calculate the total distance
full_route, total_distance = find_all_routes(routes, start_node, distances)

# Display the route and total distance
print("Route:", " -> ".join(map(str, full_route)))
print(f"Total Distance: {total_distance}")

# Convert the solution from the first part into the route_1 format
route_1 = full_route

# Load the Excel file with the coordinates from the "Nodes" sheet
excel_file_path = r"C:\Users\putta\OneDrive - Dalhousie University\Distribution Management\Projects\Final\Data\spryfield_network_data.xlsx"  # Replace with the actual path to your Excel file
df = pd.read_excel(excel_file_path, sheet_name='Nodes')

# Get the coordinates for the route
route_1_coordinates = get_route_coordinates(route_1, df)

# Create a folium map centered on the first coordinate of the route
m = folium.Map(location=route_1_coordinates[0], zoom_start=14)

# Add the route (Route 1) in blue
folium.PolyLine(route_1_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

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
