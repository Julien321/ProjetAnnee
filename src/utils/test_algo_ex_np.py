import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve



def solve_pressure_network_np(G, D, N1, N2, p_exit_value):
    num_nodes = len(G.nodes())
    A = np.zeros((num_nodes, num_nodes))
    b = np.zeros(num_nodes)

    # Mapping from node to index
    node_to_index = {node: idx for idx, node in enumerate(G.nodes())}

    for node in G.nodes():
        node_idx = node_to_index[node]
        for neighbor in G.neighbors(node):
            neighbor_idx = node_to_index[neighbor]
            A[node_idx, neighbor_idx] = -D[(node, neighbor)] / G[node][neighbor]['length']
            A[node_idx, node_idx] += D[(node, neighbor)] / G[node][neighbor]['length']

        if node == N1:
            b[node_idx] = 1
        elif node == N2:
            b[node_idx] = -1

    print("Matrice A :")
    print(A)

    # Solve the system
    pressures_solved = np.linalg.solve(A, b)

    # Convert the solution to a dictionary
    pressures_final = {node: pressures_solved[node_to_index[node]] for node in G.nodes()}

    # Adjust the pressure at the exit node
    adjustment = p_exit_value - pressures_final[N2]
    for node in pressures_final:
        pressures_final[node] += adjustment

    return pressures_final







G = nx.Graph()

# Ajouter des arêtes et des longueurs d'arêtes spécifiques
G.add_edge(1, 2, length=4)
G.add_edge(1, 3, length=12)
G.add_edge(2, 3, length=4)
G.add_edge(2, 4, length=15)
G.add_edge(3, 4, length=5)
#
# Utiliser une disposition circulaire pour visualiser le graphe
pos = nx.circular_layout(G)
#
# Dessiner le graphe
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=15)
#
# Ajouter des étiquettes aux arêtes pour montrer la longueur de chaque arête
edge_labels = nx.get_edge_attributes(G, 'length')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)
#
# Afficher le graphe
plt.title('Graphe Spécifique avec Longueurs des Arêtes')
plt.show()


# Initialisation des variables pour l'algorithme Physarum
N = G.number_of_nodes()
# Initialize D with both edge directions
D = {edge: 1 for edge in G.edges()}
D.update({(e[1], e[0]): 1 for e in G.edges()})  # Add reverse direction

# Initialisation d'une structure pour suivre l'évolution des conductivités
D_history = {edge: [] for edge in G.edges()}  # Pour chaque arête, créez une liste pour suivre les conductivités

Q = np.zeros((N, N))  # Flux à travers chaque tube
#P = np.zeros(N)  # Pression à chaque noeud
P = [None] * len(G.nodes())
cnt = 0  # Compteur d'itérations
termination_criterion = False

# Définir les nœuds de départ et de fin pour l'algorithme Physarum
N1 = 1
N2 = 4

# Algorithme Physarum
while not termination_criterion:

    for edge in D:
        if edge in D_history:
            D_history[edge].append(D[edge])

    # Définir la pression au nœud d'arrivée à 0
    P[N2 - 1] = 0  # Les indices des noeuds dans P commencent à 0

    #7
    P = solve_pressure_network_np(G,D,N1,N2,P[N2 - 1])
    print("Pressions aux noeuds après résolution : ", P)

    #8
    # Modification ici
    pressure_values = {node: pressure for node, pressure in P.items()}

    # Mise à jour des flux Qij
    for i, j in G.edges():
        print(i, j)
        pi = pressure_values[i]  # Utilisez les indices de nœuds directement
        pj = pressure_values[j]
        Lij = G[i][j]['length']
        Q[i - 1][j - 1] = D[(i, j)] * (pi - pj) / Lij
        Q[j - 1][i - 1] = -Q[i - 1][j - 1]

    # Afficher la matrice des flux Q mise à jour
    print("Flux à travers chaque tube après mise à jour : \n", Q)

    #9
    # Mise à jour des conductivités Dij en utilisant les nouvelles valeurs de pression et de flux
    for i, j in G.edges():
        pi = pressure_values[i]  # Utilisez directement les numéros de nœuds
        pj = pressure_values[j]
        Lij = G[i][j]['length']
        pN2 = pressure_values[N2]  # De même, utilisez les numéros de nœuds pour N1 et N2
        pN1 = pressure_values[N1]
        Qij = Q[i - 1][j - 1]  # Assurez-vous que l'indexation est correcte pour votre matrice Q

        # Appliquer la formule de mise à jour pour Dij
        D[(i, j)] = 0.5 * (((Qij * (pi - pj)) / (Lij * (pN1 - pN2))) + D[(i, j)])
        D[(j, i)] = D[(i, j)]  # Assurez-vous que les conductivités sont mises à jour dans les deux directions

    # Afficher les nouvelles conductivités Dij
    print("Conductivités mises à jour : ", D)

    # Vérifier le critère de terminaison (max 100 itérations pour cet exemple)
    termination_criterion = cnt >= 100
    cnt += 1



for edge, conductivities in D_history.items():
    plt.plot(conductivities, label=f'{edge}')  # Utilisez une étiquette pour identifier chaque courbe

plt.xlabel('Iterations')
plt.ylabel('Conductivity')
plt.title('Evolution of Conductivity Over Iterations')
plt.legend()  # Affiche une légende pour identifier les courbes
plt.show()