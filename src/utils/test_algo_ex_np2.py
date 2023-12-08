import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve
import random


def resoudre_systeme_avec_D(D, G):

    D12 = D[(1, 2)]
    D13 = D[(1, 3)]
    D23 = D[(2, 3)]
    D24 = D[(2, 4)]
    D34 = D[(3, 4)]


    A = np.array([
        [D13 / 12 + D12 / 4, -D12 / 4, -D13 / 12],
        [-D12 / 4, D12 / 4 + D23 / 4 + D24 / 15, -D23 / 4],
        [-D13 / 12, -D23 / 4, D13 / 12 + D23 / 4 + D34 / 5]
    ])

    # Termes constants
    b = np.array([1, 0, 0])

    # Résoudre le système
    x, y, z = np.linalg.solve(A, b)


    P = [None] * len(G.nodes())
    P[0], P[1], P[2] = x, y, z
    P[-1] = 0  # La dernière pression est toujours 0

    return P


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

D = {edge: random.random() for edge in G.edges()}
D.update({(e[1], e[0]): random.random() for e in G.edges()})


D_history = {edge: [] for edge in G.edges()}

Q = np.zeros((N, N))  # Flux à travers chaque tube

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

    # Résoudre le système et obtenir les pressions dans P
    P = resoudre_systeme_avec_D(D, G)
    print(P)

    #8
    # Modification ici
    pressure_values = P

    # Mise à jour des flux Qij
    for i, j in G.edges():
        pi = pressure_values[i - 1]  # Ajuster l'indexation
        pj = pressure_values[j - 1]
        Lij = G[i][j]['length']
        Q[i - 1][j - 1] = D[(i, j)] * (pi - pj) / Lij
        Q[j - 1][i - 1] = -Q[i - 1][j - 1]

    # Afficher la matrice des flux Q mise à jour
    print("Flux à travers chaque tube après mise à jour : \n", Q)

    # Mise à jour des conductivités Dij
    for i, j in G.edges():
        pi = pressure_values[i - 1]
        pj = pressure_values[j - 1]
        Lij = G[i][j]['length']
        pN2 = pressure_values[N2 - 1]
        pN1 = pressure_values[N1 - 1]
        Qij = Q[i - 1][j - 1]

        # Appliquer la formule de mise à jour pour Dij
        D[(i, j)] = 0.5 * (((Qij * (pi - pj)) / (Lij * (pN1 - pN2))) + D[(i, j)])
        D[(j, i)] = D[(i, j)]

    # Afficher les nouvelles conductivités Dij
    print("Conductivités mises à jour : ", D)


    termination_criterion = cnt >= 100
    cnt += 1




for edge, conductivities in D_history.items():
    plt.plot(conductivities, label=f'{edge}')  # Utilisez une étiquette pour identifier chaque courbe

plt.xlabel('Iterations')
plt.ylabel('Conductivity')
plt.title('Evolution of Conductivity Over Iterations')
plt.legend()  # Affiche une légende pour identifier les courbes
plt.show()