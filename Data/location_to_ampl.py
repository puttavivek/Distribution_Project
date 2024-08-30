import osmnx as ox
import pandas as pd
from math import atan2, degrees
import numpy as np
import os

def main():
    # Ask user for location input and file directory
    location_name = input("Enter the location name (e.g., Fairview, Halifax, Nova Scotia, Canada): ")
    save_path = input("Enter the directory where files should be saved (e.g., C:/Users/YourName/Path/): ")
    data_name = input("Enter the name of the data (e.g., fairview): ")
    text_path = os.path.join(save_path, f'{data_name}_network_data.txt')

    # Step 1: Download the road network for the specified location
    G = ox.graph_from_place(location_name, network_type='drive')

    # Step 2: Extract nodes and edges data from the graph
    nodes, edges = ox.graph_to_gdfs(G)

    # Convert the edges into a DataFrame that includes 'u' and 'v'
    edge_list = []
    for u, v, data in G.edges(data=True):
        edge_list.append({
            'u': u,
            'v': v,
            'length': float(data.get('length', 0)),  # Explicitly cast to float
            'name': data.get('name', 'Unknown'),  # Street name
            'oneway': data.get('oneway', False)  # One-way (True) or two-way (False)
        })

    edges = pd.DataFrame(edge_list)

    # Step 3: Assign unique IDs to each osmid in nodes
    nodes['UID'] = range(1, len(nodes) + 1)

    # Step 4: Use XLOOKUP-style mapping to update the edges with UID and VID from nodes
    edges['UID'] = edges['u'].map(nodes['UID'])
    edges['VID'] = edges['v'].map(nodes['UID'])

    # Step 5: Merge node coordinates to edges for bearing calculation
    edges = edges.merge(nodes[['UID', 'x', 'y']], left_on='UID', right_on='UID', suffixes=('_u', '_v'))
    edges = edges.merge(nodes[['UID', 'x', 'y']], left_on='VID', right_on='UID', suffixes=('', '_v'))

    # Step 6: Add direction information for one-way roads (bearing from u to v)
    def calculate_bearing(x1, y1, x2, y2):
        angle = atan2(y2 - y1, x2 - x1)
        bearing = degrees(angle)
        return (bearing + 360) % 360  # Normalize bearing to [0, 360] degrees

    edges['bearing'] = edges.apply(
        lambda row: calculate_bearing(row['x'], row['y'], row['x_v'], row['y_v']) if row['oneway'] else None,
        axis=1
    )

    # Step 7: Combine nodes and edges into one Excel file with separate sheets
    network_data_path = os.path.join(save_path, f'{data_name}_network_data.xlsx')
    with pd.ExcelWriter(network_data_path) as writer:
        nodes.to_excel(writer, sheet_name='Nodes', index=True)
        edges.to_excel(writer, sheet_name='Edges', index=False)

    # Step 8: Create a distance matrix between all UIDs and VIDs
    uids = sorted(nodes['UID'].values)
    distance_matrix = pd.DataFrame(0.0, index=uids, columns=uids, dtype=float)  # Initialize with float type

    for _, row in edges.iterrows():
        u, v, length = row['UID'], row['VID'], row['length']
        if pd.isna(u) or pd.isna(v):
            continue  # Skip rows with NaN indices
        u, v = int(u), int(v)  # Ensure they are integers
        distance_matrix.at[u, v] = length
        if not row['oneway']:
            distance_matrix.at[v, u] = length  # For undirected roads

    # Replace any remaining NaNs in the distance matrix with 0
    distance_matrix.fillna(0, inplace=True)

    # Save the distance matrix to the same Excel file
    with pd.ExcelWriter(network_data_path, mode='a') as writer:
        distance_matrix.to_excel(writer, sheet_name='Distance Matrix')

    # Save the nodes, edges, and distance matrix data to a text file
    with open(text_path, 'w') as text_file:
        text_file.write("Nodes:\n")
        nodes.to_string(text_file)
        text_file.write("\n\nEdges:\n")
        edges.to_string(text_file)
        text_file.write("\n\nDistance Matrix:\n")
        distance_matrix.to_string(text_file)

    # Step 9: Plot the road network graph and save the image
    fig, ax = ox.plot_graph(G, show=False, close=False)
    fig.savefig(os.path.join(save_path, f'{data_name}.png'), dpi=300)

    # Optional: Print first few rows to check the data
    print("Nodes Data:")
    print(nodes.head())
    print("\nEdges Data:")
    print(edges.head())
    print("\nDistance Matrix:")
    print(distance_matrix.head())

    # Part 2: Prepare the data to be saved in data.py file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file_path = os.path.join(project_root, 'Chinese-Postman-master', 'data', 'data.py')

    if not os.path.exists(data_file_path):
        print(f"Error: The file '{data_file_path}' does not exist.")
        return

    with open(data_file_path, 'r') as f:
        lines = f.readlines()

    data_exists = False
    start_line = None
    end_line = None

    # Check if the data_name already exists
    for i, line in enumerate(lines):
        if line.startswith(f"{data_name} = ["):
            data_exists = True
            start_line = i
        if data_exists and line.strip() == "]":
            end_line = i + 1
            break

    # Prepare the data string to be written
    data_string = f"{data_name} = [\n"
    for edge in edges.itertuples():
        u = int(edge.UID) if not pd.isna(edge.UID) else None
        v = int(edge.VID) if not pd.isna(edge.VID) else None
        length = edge.length
        if u is None or v is None or pd.isna(length):
            continue  # Skip if there's still any NaN value
        if edge.oneway:
            data_string += f"    ({u}, {v}, {length}, True),\n"
        else:
            data_string += f"    ({u}, {v}, {length}),\n"
    data_string += "]\n"

    # Write the data to data.py
    if data_exists:
        # Replace the existing data
        lines = lines[:start_line] + [data_string] + lines[end_line:]
    else:
        # Append the new data
        lines.append("\n" + data_string)

    with open(data_file_path, 'w') as f:
        f.writelines(lines)

    print(f"Data for '{data_name}' saved to '{data_file_path}'")

    # Part 3: Run the main.py script with the data_name, save_path, and text_path as arguments
    main_py_output_path = os.path.join(save_path, f'{data_name}_output.xlsx')
    os.system(f"python {os.path.join(project_root, 'Chinese-Postman-master', 'main.py')} {data_name} --save_path \"{main_py_output_path}\" --text_path \"{text_path}\"")

if __name__ == "__main__":
    main()
