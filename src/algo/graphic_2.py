import pandas as pd
import matplotlib.pyplot as plt

# Lire les données du fichier CSV
df = pd.read_csv('../experiments/results.csv')

# Filter data for Physarum Polycephalum and Dijkstra algorithms
df_physarum = df[df['Algorithm'] == 'Physarum Polycephalum']
df_dijkstra = df[df['Algorithm'] == 'Dijkstra']

# Merge the dataframes on Start Node and End Node to align the points
df_merged = pd.merge(df_physarum, df_dijkstra, on=['Start Node', 'End Node'], suffixes=('_Physarum', '_Dijkstra'))


# Calculate average execution times
avg_time_physarum = df_merged['Execution Time (s)_Physarum'].mean()
avg_time_dijkstra = df_merged['Execution Time (s)_Dijkstra'].mean()

# Create the plot
plt.figure(figsize=(12, 8))

# Plot execution times for Physarum Polycephalum
plt.plot(df_merged.index, df_merged['Execution Time (s)_Physarum'], label='Physarum Polycephalum', marker='o')

# Plot execution times for Dijkstra
plt.plot(df_merged.index, df_merged['Execution Time (s)_Dijkstra'], label='Dijkstra', marker='o')

 #Plot average execution times
plt.axhline(y=avg_time_physarum, color='r', linestyle='--', label=f'Average Physarum Polycephalum: {avg_time_physarum:.4f}s')
plt.axhline(y=avg_time_dijkstra, color='b', linestyle='--', label=f'Average Dijkstra: {avg_time_dijkstra:.4f}s')

# Set a logarithmic scale for the y-axis
plt.yscale('log')

# Add titles and labels
plt.title('Execution Time per Iteration (for both algorithms)')
plt.xlabel('Iterations')
plt.ylabel('Execution Time (s) (Log Scale)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()