import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

# Créer un graphe connecté avec 10 nœuds
num_nodes = 10
num_edges = max(15, num_nodes - 1)  # Assurer un nombre minimum de bords pour la connectivité

# Initialiser le graphe
G = nx.Graph()

# Ajouter des nœuds au graphe
G.add_nodes_from(range(num_nodes))

# Premièrement, créer un arbre en connectant tous les nœuds, assurant la connectivité
for i in range(num_nodes - 1):
    G.add_edge(i, i + 1, length=random.randint(1, 10))

# Ajouter des bords aléatoires au graphe jusqu'à atteindre le nombre souhaité de bords
while G.number_of_edges() < num_edges:
    u, v = random.sample(list(G.nodes()), 2)
    if not G.has_edge(u, v):
        G.add_edge(u, v, length=random.randint(1, 10))

for u, v, data in G.edges(data=True):
    print(f"Longueur entre {u} et {v} : {data['length']}")

# Utiliser le layout spring pour visualiser le graphe
pos = nx.spring_layout(G)

# Dessiner le graphe
nx.draw(G, pos, with_labels=True, edge_color='black', node_size=500, node_color='pink')

# Ajouter des étiquettes aux arêtes pour montrer la longueur de chaque arête
edge_labels = nx.get_edge_attributes(G, 'length')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title('Graphe Connecté Aléatoire')
plt.show()

# Définir les nœuds de départ et de fin pour l'algorithme Physarum
N1 = 0
N2 = num_nodes - 1

# Initialisation des paramètres de l'algorithme
D = np.random.uniform(0, 1, (num_nodes, num_nodes))  # Matrice de conductivité
Q = np.zeros((num_nodes, num_nodes))  # Matrice de flux
P = np.zeros(num_nodes)  # Vecteur de pression
# Créer un dictionnaire pour stocker la longueur de l'arête entre chaque paire de nœuds
L = {(u, v): data['length'] for u, v, data in G.edges(data=True)}


# Imprimer la longueur de chaque arête dans le graphe
for u, v, data in G.edges(data=True):
    print(f"Longueur entre {u} et {v} : {data['length']}")

# Algorithme Physarum
# Algorithme Physarum
def physarum_algo(G, D, Q, P, L, N1, N2, iterations=100):
    for iteration in range(iterations):
        # Mise à jour des pressions
        for i in G.nodes():
            if i == N1:
                P[i] = 1
            elif i == N2:
                P[i] = 0
            else:
                # Utiliser une liste de compréhension pour calculer la somme des pressions
                P[i] = sum(D[i, j] / L[(min(i, j), max(i, j))] * (P[i] - P[j]) for j in G.neighbors(i))

        # Mise à jour des flux
        for i, j in G.edges():
            Q[i, j] = D[i, j] * (P[i] - P[j]) / L[(min(i, j), max(i, j))]

        # Mise à jour des conductivités
        for i, j in G.edges():
            # Assurer l'ordre correct des indices pour les clés du dictionnaire L
            edge_key = (min(i, j), max(i, j))
            D[i, j] = (Q[i, j] * (P[i] - P[j]) / L[edge_key] + D[i, j]) / 2

# Exécuter l'algorithme Physarum
physarum_algo(G, D, Q, P, L, N1, N2)


# Dessiner le graphe entier en premier
nx.draw(G, pos, with_labels=True, edge_color='black', node_size=500, node_color='pink')

# Ensuite, trouver le chemin le plus court après l'exécution de l'algorithme
shortest_path = nx.shortest_path(G, source=N1, target=N2, weight='length')

# Mettre en évidence les arêtes du chemin le plus court en rouge
path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

# Mettre en évidence les nœuds du chemin le plus court en rouge
nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='red', node_size=500)

# Afficher le graphe complet avec le chemin le plus court mis en évidence
plt.title('Graphe Connecté Aléatoire avec Chemin le Plus Court')
plt.show()

