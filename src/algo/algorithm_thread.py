from PyQt5.QtCore import QThread, pyqtSignal
from src.algo.physarum_polycephalum import *
import time
import matplotlib.pyplot as plt
from src.algo.experiment import save_experiment_result


class AlgorithmThread(QThread):
    count_updated = pyqtSignal(int)
    finished_signal = pyqtSignal(list)
    time_elapsed_signal = pyqtSignal(float)  # Signal pour le temps écoulé

    total_length_signal = pyqtSignal(float)  # Ajout d'un signal pour la longueur totale
    conductivity_updated = pyqtSignal(dict)

    def __init__(self, graph, N1, N2, numIterations):
        super().__init__()
        self.G = graph
        self.N1 = N1
        self.N2 = N2
        self.numIterations = numIterations


    def run(self):
        start_time = time.perf_counter()  # Démarrer le compteur
        cnt = 0
        while cnt < self.numIterations:
            P = solve_linear_equation(self.G, self.N1, self.N2)

            # Mettre à jour les flux sur les arêtes en fonction des pressions calculées
            update_fluxes(self.G, P)

            # Après avoir calculé les pressions et mis à jour les flux, mettez à jour les conductivités
            update_conductivities(self.G, P, self.N1, self.N2)

            self.count_updated.emit(cnt)

            current_conductivities = {edge: self.G[edge[0]][edge[1]]['conductivity'] for edge in self.G.edges()}
            self.conductivity_updated.emit(current_conductivities)  # Émettre les conductivités actuelles

            cnt += 1

        print(current_conductivities)
        end_time = time.perf_counter()  # Arrêter le compteur
        # Liste pour stocker les arêtes avec leur Dij
        edges_with_Dij = []

        # Parcourir toutes les arêtes et stocker leur Dij
        for (i, j) in self.G.edges():
            Dij = self.G[i][j]['conductivity']
            edges_with_Dij.append((i, j, Dij))

        # Trier la liste en fonction de Dij dans un ordre décroissant
        edges_with_Dij.sort(key=lambda x: x[2], reverse=True)

        # Sélectionner les plus grands Dij
        top_10_Dij = edges_with_Dij[:300]
        print(top_10_Dij)

        selected_edges = create_path2(top_10_Dij, self.N1, self.N2)

        # Calculer la longueur totale du chemin trouvé
        total_length = sum(self.G[edge[0]][edge[1]]['length'] for edge in selected_edges)

        # Afficher les résultats
        for edge in selected_edges:
            print(f"Arête entre {edge[0]} et {edge[1]}, Dij = {self.G[edge[0]][edge[1]]['conductivity']}")

        # Créer une liste des noeuds impliqués
        list_of_nodes = []
        for edge in selected_edges:
            list_of_nodes.append(edge[0])
            list_of_nodes.append(edge[1])

        print(list_of_nodes)
        #time
        elapsed_time = end_time - start_time  # Calculer le temps écoulé
        print(f"L'algorithme a pris {elapsed_time:.2f} secondes.")
        print(f"Longueur totale du chemin trouvé : {total_length}")




        self.time_elapsed_signal.emit(elapsed_time)  # Émettre le signal avec le temps écoulé

        # Enregistrer les résultats dans le fichier CSV
        save_experiment_result(self.N1, self.N2, elapsed_time, total_length,self.numIterations,algo= "Physarum Polycephalum")

        self.finished_signal.emit(selected_edges)





