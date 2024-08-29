import pandas as pd

# Load the Excel file
excel_file = r"C:\Users\putta\OneDrive - Dalhousie University\Distribution Management\Projects\Data\X\fairview.xlsx"  # Replace with the path to your actual Excel file
df = pd.read_excel(excel_file)

# Extract necessary columns (u, v, length, oneway)
u_column = df['UID']
v_column = df['VID']
length_column = df['length']
oneway_column = df['oneway']

# Prepare the set of edges to avoid duplicates
edges = set()

for u, v, length, oneway in zip(u_column, v_column, length_column, oneway_column):
    # Check and handle NaN values in 'u', 'v', and 'length'
    if pd.isna(u) or pd.isna(v) or pd.isna(length):
        print(f"Skipping row with NaN values: u={u}, v={v}, length={length}")
        continue  # Skip rows with NaN values

    # Ensure 'u' and 'v' are treated as integers
    try:
        u = int(u)
        v = int(v)
        length = float(length)
    except ValueError as e:
        print(f"Error converting values: u={u}, v={v}, length={length}, error={e}")
        continue

    # Skip adding (v, u) if (u, v) already exists
    if (v, u) in edges:
        continue

    # Add the edge (u, v) and (v, u) if it's not one-way
    if oneway:
        edges.add((u, v, length, True))  # Directed edge
    else:
        edges.add((u, v, length))  # Undirected edge
        edges.add((v, u, length))  # Add reverse as undirected

# Save the edges in the format suitable for the Chinese Postman program
with open('../graph_data.py', 'w') as f:
    f.write("fairview = [\n")
    for edge in edges:
        if len(edge) == 4:  # Directed edge
            f.write(f"    ({edge[0]}, {edge[1]}, {edge[2]}, {edge[3]}),\n")
        else:  # Undirected edge
            f.write(f"    ({edge[0]}, {edge[1]}, {edge[2]}),\n")
    f.write("]\n")

print("Graph data saved to 'graph_data.py'")
