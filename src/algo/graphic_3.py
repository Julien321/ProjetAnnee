import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Lire les données à partir du fichier CSV
file_path = '../experiments/results.csv'
data = pd.read_csv(file_path)

# Extraire les longueurs pour chaque algorithme
physarum_lengths = data[data['Algorithm'] == 'Physarum Polycephalum']['Path Length (m)'].tolist()
dijkstra_lengths = data[data['Algorithm'] == 'Dijkstra']['Path Length (m)'].tolist()

# Assurez-vous que les deux listes ont la même longueur et correspondent aux mêmes paires de points
min_length = min(len(physarum_lengths), len(dijkstra_lengths))
physarum_lengths = physarum_lengths[:min_length]
dijkstra_lengths = dijkstra_lengths[:min_length]

# Générer des couleurs et symboles uniques pour chaque paire
colors = plt.cm.rainbow(np.linspace(0, 1, len(physarum_lengths)))
symbols = ['o', 's', 'D', '^', 'v', '>', '<', 'p', 'h', '*'] * (len(physarum_lengths) // 10 + 1)

# Générer les positions aléatoires pour la dispersion horizontale
positions = np.random.normal(0, 0.1, len(physarum_lengths))

# Création du box plot
data = [physarum_lengths, dijkstra_lengths]

plt.figure(figsize=(10, 6))
plt.boxplot(data, notch=True, vert=True, patch_artist=False, labels=['Physarum', 'Dijkstra'])

# Ajouter des points individuels avec les mêmes couleurs et symboles pour chaque paire
for i in range(len(physarum_lengths)):
    # Points pour Physarum
    plt.scatter(1 + positions[i], physarum_lengths[i], color=colors[i], marker=symbols[i], alpha=0.7)
    # Points pour Dijkstra
    plt.scatter(2 + positions[i], dijkstra_lengths[i], color=colors[i], marker=symbols[i], alpha=0.7)

plt.ylabel('Path Length (m)')
plt.title('Best path length over 50 instances chosen at random')
plt.show()
