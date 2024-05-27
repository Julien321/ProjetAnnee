import os
import csv


def save_experiment_result(start_node, end_node, execution_time, path_length,numIterations,algo):
    # Vérifier si le dossier 'experiments' existe, sinon le créer
    if not os.path.exists('experiments'):
        os.makedirs('experiments')

    # Définir le chemin du fichier CSV
    csv_file_path = os.path.join('experiments', 'results.csv')

    # Vérifier si le fichier CSV existe déjà
    file_exists = os.path.isfile(csv_file_path)

    # Ouvrir le fichier en mode ajout (append)
    with open(csv_file_path, mode='a', newline='') as csvfile:
        fieldnames = [ 'Algorithm','Start Node', 'End Node','Iterations', 'Execution Time (s)', 'Path Length (m)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Écrire l'en-tête si le fichier est nouveau
        if not file_exists:
            writer.writeheader()

        # Arrondir path_length à la centième près
        rounded_path_length = round(path_length, 2)

        # Écrire les données de l'expérience
        writer.writerow({
            'Algorithm' : algo,
            'Start Node': start_node,
            'End Node': end_node,
            'Iterations':numIterations,
            'Execution Time (s)': execution_time,
            'Path Length (m)': rounded_path_length
        })
