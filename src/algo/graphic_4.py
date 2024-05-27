import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Lire les données à partir du fichier CSV
file_path = '../experiments/results.csv'
data = pd.read_csv(file_path)

# Extraire les longueurs pour chaque algorithme
physarum_data = data[data['Algorithm'] == 'Physarum Polycephalum']
dijkstra_data = data[data['Algorithm'] == 'Dijkstra']

# Assurez-vous que les deux listes ont la même longueur et correspondent aux mêmes paires de points
min_length = min(len(physarum_data), len(dijkstra_data))
physarum_lengths = physarum_data['Path Length (m)'].tolist()[:min_length]
dijkstra_lengths = dijkstra_data['Path Length (m)'].tolist()[:min_length]

# Filtrer les paires de points dont les longueurs diffèrent
physarum_filtered = []
dijkstra_filtered = []
for pl, dl in zip(physarum_lengths, dijkstra_lengths):
    if pl != dl:
        physarum_filtered.append(pl)
        dijkstra_filtered.append(dl)

# Générer des couleurs et symboles uniques pour chaque paire
colors = plt.cm.rainbow(np.linspace(0, 1, len(physarum_filtered)))
symbols = ['o', 's', 'D', '^', 'v', '>', '<', 'p', 'h', '*'] * (len(physarum_filtered) // 10 + 1)

# Générer les positions aléatoires pour la dispersion horizontale
positions = np.random.normal(0, 0.1, len(physarum_filtered))

# Création du box plot
data = [physarum_filtered, dijkstra_filtered]

plt.figure(figsize=(10, 6))
plt.boxplot(data, notch=True, vert=True, patch_artist=False, labels=['Physarum', 'Dijkstra'])

# Ajouter des points individuels avec les mêmes couleurs et symboles pour chaque paire
for i in range(len(physarum_filtered)):
    # Points pour Physarum
    plt.scatter(1 + positions[i], physarum_filtered[i], color=colors[i], marker=symbols[i], alpha=0.7)
    # Points pour Dijkstra
    plt.scatter(2 + positions[i], dijkstra_filtered[i], color=colors[i], marker=symbols[i], alpha=0.7)

plt.ylabel('Path Length(m)')
plt.title('Best path length on instances with different lengths')
plt.show()
