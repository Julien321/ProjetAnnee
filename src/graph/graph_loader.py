import json
import networkx as nx
import random


def load_graph(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Créer un graphe simple non orienté
    G = nx.Graph()

    # Ajouter des nœuds avec leurs ID
    for node_data in data['nodes']:
        G.add_node(node_data['id'], **node_data)

    # Ajouter des arêtes avec vérification de la plus petite longueur
    for edge_data in data['links']:
        u, v = edge_data['source'], edge_data['target']
        length = edge_data['length']
        if G.has_edge(u, v):
            # Si une arête existe déjà, garder celle avec la plus petite longueur
            if G[u][v]['length'] > length:
                G[u][v]['length'] = length
        else:
            # Ajouter l'arête avec les attributs de conductivité et de flux
            G.add_edge(u, v, length=length, conductivity=random.uniform(0, 1), flux=0)

    return G

