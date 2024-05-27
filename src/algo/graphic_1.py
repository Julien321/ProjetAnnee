import pandas as pd
import matplotlib.pyplot as plt

# Lire les données du fichier CSV
df = pd.read_csv('../experiments/results.csv')

# Créer une nouvelle colonne pour le numéro de la ligne
df['Line Number'] = (df.index / 2) + 1

# Filtrer les données pour les algorithmes Physarum Polycephalum et Dijkstra
df_physarum = df[df['Algorithm'] == 'Physarum Polycephalum']
#df_dijkstra = df[df['Algorithm'] == 'Dijkstra']

# Calculer la moyenne des temps d'exécution pour chaque algorithme
mean_physarum = df_physarum['Execution Time (s)'].mean()
#mean_dijkstra = df_dijkstra['Execution Time (s)'].mean()

# Créer le graphique
plt.figure(figsize=(12, 8))

# Tracer les temps d'exécution pour Physarum Polycephalum
plt.plot(df_physarum['Line Number'], df_physarum['Execution Time (s)'], label='Physarum Polycephalum', marker='o')

# Tracer les temps d'exécution pour Dijkstra
#plt.plot(df_dijkstra['Line Number'], df_dijkstra['Execution Time (s)'], label='Dijkstra', marker='o')

# Ajouter une ligne pour la moyenne des temps d'exécution pour Physarum Polycephalum
plt.axhline(mean_physarum, color='red', linestyle='--', linewidth=1, label=f'Average Physarum Polycephalum: {mean_physarum:.4f}s')

# Ajouter une ligne pour la moyenne des temps d'exécution pour Dijkstra
#plt.axhline(mean_dijkstra, color='orange', linestyle='--', linewidth=1, label='Moyenne Dijkstra')

# Ajouter des titres et des labels
plt.title('Execution Time per Iteration')
plt.xlabel('Iterations')
plt.ylabel('Execution Time (s)')
plt.legend()
plt.grid(True)

# Afficher le graphique
plt.show()

