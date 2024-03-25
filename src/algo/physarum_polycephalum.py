import numpy as np
import networkx as nx


def update_fluxes(G, P):
    # Parcourir toutes les arêtes du graphe et mettre à jour les flux
    for (i, j) in G.edges():
        D_ij = G[i][j]['conductivity']  # Conductivité de l'arête
        L_ij = G[i][j]['length']  # Longueur de l'arête
        p_i = P[i]  # Pression au nœud i
        p_j = P[j]  # Pression au nœud j

        # Calculer le flux Q_ij en utilisant la formule fournie
        Q_ij = D_ij * (p_i - p_j) / L_ij

        # Mettre à jour le flux de l'arête dans le graphe
        G[i][j]['flux'] = Q_ij


def update_conductivities(G, P, N1, N2):
    # Parcourir toutes les arêtes du graphe et mettre à jour les conductivités
    for (i, j) in G.edges():
        Q_ij = G[i][j]['flux']  # Flux actuel de l'arête
        D_ij = G[i][j]['conductivity']  # Conductivité actuelle de l'arête
        L_ij = G[i][j]['length']  # Longueur de l'arête


        p_i = P[i]  # Pression au nœud i
        p_j = P[j]  # Pression au nœud j
        p_N1 = P[N1]  # Pression au nœud de départ N1
        p_N2 = P[N2]  # Pression au nœud d'arrivée N2

        # Calculer la nouvelle conductivité D_ij en utilisant la formule fournie
        new_D_ij = 0.5 * ((Q_ij * (p_i - p_j)) / (L_ij * (p_N1 - p_N2)) + D_ij)

        # Mettre à jour la conductivité de l'arête dans le graphe
        G[i][j]['conductivity'] = new_D_ij


def solve_linear_equation(G, N1, N2):
    # Exclure le noeud N2
    nodes = [node for node in G.nodes() if node != N2]
    num_nodes = len(nodes)

    # Initialiser la matrice A avec des zéros
    A = np.zeros((num_nodes, num_nodes))

    # Mapping des noeuds aux indices de la matrice
    node_to_index = {node: idx for idx, node in enumerate(nodes)}

    # Construire la matrice A
    for i in nodes:
        idx_i = node_to_index[i]
        for j in G.nodes():  # Inclure N2 pour les termes diagonaux
            if i != j and G.has_edge(i, j):  # Vérifier si l'arête entre i et j existe
                Dij = G[i][j]['conductivity']
                Lij = G[i][j]['length']
                if j != N2:  # Ajouter le terme hors diagonale si j n'est pas N2
                    idx_j = node_to_index[j]
                    A[idx_i][idx_j] = -Dij / Lij
                A[idx_i][idx_i] += Dij / Lij  # Ajouter le terme diagonal

    # Initialiser et définir le vecteur b pour N1
    b = np.zeros(num_nodes)
    b[node_to_index[N1]] = 1  # Source à N1


    pressures_values = np.linalg.solve(A, b)


    # Créer le dictionnaire des pressions avec la pression à N2 fixée à 0
    pressures = {node: (0 if node == N2 else pressures_values[node_to_index[node]]) for node in nodes}
    pressures[N2] = 0  # La pression en N2 est fixée à 0

    return pressures


def create_path(edge_list, N1, N2):
    # Créer un graphe temporaire pour suivre le chemin
    temp_graph = nx.Graph()
    # Liste pour les arêtes sélectionnées
    selected_edges = []

    for i, j, _ in edge_list:

        # Ajouter l'arête au graphe temporaire
        temp_graph.add_edge(i, j)

        selected_edges.append((i, j))

        # Vérifier si un chemin complet est formé
        if N1 in temp_graph and N2 in temp_graph:
            for edge in temp_graph.edges():
                print("edge = ",edge)
            if nx.has_path(temp_graph, N1, N2):
                break
    return selected_edges

def create_path2(edge_list, N1, N2):
    # Créer un graphe temporaire pour suivre le chemin
    temp_graph = nx.Graph()
    # Liste pour les arêtes sélectionnées
    selected_edges = []

    for i, j, _ in edge_list:
        # Ajouter l'arête au graphe temporaire
        temp_graph.add_edge(i, j)
        selected_edges.append((i, j))

        # Vérifier si un chemin complet est formé
        if N1 in temp_graph and N2 in temp_graph:
            if nx.has_path(temp_graph, N1, N2):
                # Trouver le chemin et ne conserver que les arêtes qui y contribuent
                path = nx.shortest_path(temp_graph, N1, N2)
                path_edges = list(zip(path[:-1], path[1:]))
                selected_edges = [edge for edge in selected_edges if edge in path_edges or (edge[1], edge[0]) in path_edges]
                break

    return selected_edges