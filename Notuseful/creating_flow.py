from collections import defaultdict

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

def find_all_routes(routes, start_node, distances):
    # Stack for DFS and result list to store the final loop
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

# Load routes from the text file
file_path = r"../Data/AMPLoutput.txt"  # Replace with actual path
routes, distances = read_routes_from_file(file_path)

# Specify the starting node
start_node = int(input("Enter the starting node: "))

# Generate the route and calculate the total distance
full_route, total_distance = find_all_routes(routes, start_node, distances)

# Display the route and total distance
print("Route:", " -> ".join(map(str, full_route)))
print(f"Total Distance: {total_distance}")
