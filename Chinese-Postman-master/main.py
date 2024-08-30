import argparse
import sys
import numpy as np
import pandas as pd
import data.data
from chinesepostman import eularian, network


def setup_args():
    """Setup argparse to take graph name, start node, and save path arguments."""
    parser = argparse.ArgumentParser(description='Find an Eulerian Circuit.')
    parser.add_argument('graph', help='Name of graph to load')
    parser.add_argument(
        '--start',
        type=int,
        default=None,
        help='The starting node. Random if none provided.'
    )
    parser.add_argument(
        '--save_path',
        type=str,
        default='graph_output.xlsx',
        help='Directory where the Excel file should be saved (e.g., C:/Users/YourName/Path/graph_output.xlsx)'
    )
    args = parser.parse_args()
    return args


def convert_graph_to_sets_and_matrix(graph, num_nodes):
    directed_edges = []
    undirected_edges = set()  # Use a set to avoid adding both (u, v) and (v, u)

    # Create an empty distance matrix with 0s
    distance_matrix = np.zeros((num_nodes, num_nodes))

    # Iterate over the edges in the graph
    for edge in graph.edges.values():
        u, v, weight, directed = edge.head, edge.tail, edge.weight, edge.directed
        if directed:
            directed_edges.append((u, v))  # Directed edge (u, v)
            distance_matrix[u - 1][v - 1] = weight  # Directed distance
        else:
            # Ensure that only (u, v) or (v, u) is added once by using a sorted tuple
            edge_tuple = tuple(sorted((u, v)))  # Sorting ensures that (u, v) and (v, u) are treated as the same
            if edge_tuple not in undirected_edges:
                undirected_edges.add(edge_tuple)  # Add the edge as a tuple
                distance_matrix[u - 1][v - 1] = weight
                distance_matrix[v - 1][u - 1] = weight  # Symmetric for undirected

    # Convert the undirected_edges set back to a list of tuples
    undirected_edges_list = [(u, v) for u, v in undirected_edges]

    return directed_edges, undirected_edges_list, distance_matrix


def save_to_excel(directed_edges, undirected_edges, distance_matrix, save_path):
    """Save directed set, undirected set, and distance matrix to an Excel file."""
    with pd.ExcelWriter(save_path) as writer:
        # Convert directed edges to a formatted string and save to sheet
        directed_str = "set A_d := " + " ".join(f"({u},{v})" for u, v in directed_edges) + " ;"
        df_directed = pd.DataFrame([directed_str], columns=['Directed Edges'])
        df_directed.to_excel(writer, sheet_name='Directed_Edges', index=False)

        # Convert undirected edges to a formatted string and save to sheet
        undirected_str = "set A_u := " + " ".join(f"({u},{v})" for u, v in undirected_edges) + " ;"
        df_undirected = pd.DataFrame([undirected_str], columns=['Undirected Edges'])
        df_undirected.to_excel(writer, sheet_name='Undirected_Edges', index=False)

        # Save distance matrix to a sheet with rows and columns starting from 1
        df_matrix = pd.DataFrame(distance_matrix,
                                 index=range(1, distance_matrix.shape[0] + 1),  # Set index starting from 1
                                 columns=range(1, distance_matrix.shape[1] + 1))  # Set columns starting from 1
        df_matrix.to_excel(writer, sheet_name='Distance_Matrix', index=True)

    print(f'Data saved to {save_path}')


def main():
    """Main function to compute and return the Eulerized graph and solve the Chinese Postman Problem."""
    edges = None
    args = setup_args()
    graph_name = args.graph
    save_path = args.save_path

    try:
        print(f'Loading graph: {graph_name}')
        edges = getattr(data.data, graph_name)
    except (AttributeError, TypeError):
        available = [x for x in dir(data.data) if not x.startswith('__')]
        print(
            '\nInvalid graph name.'
            ' Available graphs:\n\t{}\n'.format('\n\t'.join(available))
        )
        sys.exit()

    original_graph = network.Graph(edges)

    print(f'<{len(original_graph.edges)}> edges loaded')
    if not original_graph.is_eularian:
        print('Converting to Eulerian path...')
        graph, num_dead_ends = eularian.make_eularian(original_graph)
        print('Conversion complete')
        print(f'\tAdded {len(graph.edges) - len(original_graph.edges) + num_dead_ends} edges')
        print(f'\tTotal cost is {graph.total_cost}')
    else:
        graph = original_graph
        print("Graph is already Eulerian")

    # Number of nodes (intersections)
    num_nodes = len(original_graph.nodes)

    # Convert the graph to sets of directed and undirected edges and a distance matrix
    directed_edges, undirected_edges, distance_matrix = convert_graph_to_sets_and_matrix(graph, num_nodes)

    # Save the directed, undirected edges and distance matrix to an Excel file
    save_to_excel(directed_edges, undirected_edges, distance_matrix, save_path)

    # Attempt to solve Eulerian Circuit
    print('Attempting to solve Eulerian Circuit...')
    route, attempts = eularian.eularian_path(graph, args.start)
    if not route:
        print(f'\tGave up after <{attempts}> attempts.')
    else:
        print(f'\tSolved in <{attempts}> attempts')
        print(f'Solution: (<{len(route) - 1}> edges)')
        print(f'\t{route}')
    print(graph)
    return graph  # This returns the modified Eulerized graph


if __name__ == '__main__':
    main()
