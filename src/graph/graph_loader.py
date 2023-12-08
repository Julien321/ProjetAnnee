import json
import networkx as nx

def load_graph(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return nx.node_link_graph(data)
