import networkx as nx
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

# Utiliser le layout spring pour visualiser le graphe
pos = nx.spring_layout(G)

# Dessiner le graphe
nx.draw(G, pos, with_labels=True, edge_color='black', node_size=500, node_color='pink')
plt.title('Graphe Connecté Aléatoire')
plt.show()

# Exécutez votre algorithme Physarum ici pour mettre à jour le graphe G (omis pour la brièveté)
# ...

# Après avoir exécuté l'algorithme, trouvez le chemin le plus court
# Pour l'exemple, nous utilisons Dijkstra pour trouver le chemin le plus court
start_node, end_node = 0, num_nodes - 1  # Nœuds de départ et de fin pour l'exemple
shortest_path = nx.dijkstra_path(G, start_node, end_node, weight='length')

# Dessiner le graphe à nouveau après avoir exécuté l'algorithme
nx.draw(G, pos, with_labels=True, edge_color='black', node_size=500, node_color='lightblue')

# Mettre en évidence le chemin le plus court en rouge
path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
plt.title('Graphe Connecté Aléatoire avec Chemin le Plus Court')
plt.show()
