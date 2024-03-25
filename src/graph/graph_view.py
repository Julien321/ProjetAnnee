from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt
from src.gui.clickable_node import ClickableNode
from src.gui.clickable_button import ClickableButton
from src.gui.clear_button import ClearButton
from src.graph.graph_loader import load_graph
from functools import partial
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsLineItem
from src.algo.algorithm_thread import AlgorithmThread
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer
import networkx as nx

from PyQt5.QtWidgets import QInputDialog

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor


import time


class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(Qt.black)
        self.setScene(self.scene)
        self.setRenderHints(QPainter.Antialiasing)

        self.G = None
        self.init_graph_view()

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoomRange = [0, 10]
        self.zoomLevel = 0

        self.selected_nodes = []
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self._isPanning = False
        self._panStartX = 0
        self._panStartY = 0

        # Créer et positionner le bouton
        self.button = ClickableButton('PhysarumPolycephalum', self)
        self.button.clicked_signal.connect(self.on_button_clicked)
        self.button.setGeometry(self.viewport().width() - 100, self.viewport().height() - 50, 200, 30)

        # Nouveau bouton pour l'algorithme Dijkstra
        self.dijkstra_button = QPushButton('Dijkstra', self)  # Création du bouton
        self.dijkstra_button.clicked.connect(self.on_dijkstra_button_clicked)  # Connexion du signal à la slot
        self.button.setGeometry(self.viewport().width() - 100, self.viewport().height() - 50, 200, 30)

        # Créer un bouton "Clear"
        self.clear_button = ClearButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_graph)
        self.clear_button.setGeometry(self.viewport().width() - 100, self.viewport().height() - 50, 80, 30)

        # Ajouter un QLabel pour afficher le count
        self.count_label = QLabel(self)
        self.count_label.setGeometry(10, 10, 50, 30)
        self.count_label.setStyleSheet("color: red; font-size: 16pt;")

        """
        #time
        self.time_label = QLabel(self)
        self.time_label.setGeometry(10, 10, 500, 300)  # Positionnez et redimensionnez selon vos besoins
        self.time_label.setStyleSheet("color: red; font-size: 16pt;")  # Mettre le texte en rouge

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_label)

        self.start_time = None
        """

    def init_graph_view(self):
        self.G = load_graph("data/BRU.json")
        scale = 10000
        pen = QPen(Qt.green)
        pen.setWidth(0)

        for node_id in self.G.nodes():
            node_data = self.G.nodes[node_id]
            node_item = ClickableNode(node_data['x'] * scale, -node_data['y'] * scale, 3, 3, node_id, self)
            node_item.clicked.connect(partial(self.node_clicked, node_id))
            self.scene.addItem(node_item.graphics_item)

        for edge in self.G.edges():
            source_node = self.G.nodes[edge[0]]
            target_node = self.G.nodes[edge[1]]
            line = QGraphicsLineItem(source_node['x'] * scale, -source_node['y'] * scale, target_node['x'] * scale, -target_node['y'] * scale)
            line.setPen(pen)

            line.setData(0, edge)

            self.scene.addItem(line)

    def clear_graph(self):
        # Nettoyer la scène graphique
        self.scene.clear()

        # Réinitialiser la liste des noeuds sélectionnés si elle existe
        self.selected_nodes = []

        # Recharger le graphe
        self.init_graph_view()

    def resizeEvent(self, event):
        # Redimensionner et repositionner les boutons lors du redimensionnement de la fenêtre
        super().resizeEvent(event)
        self.clear_button.setGeometry(self.viewport().width() -1250, self.viewport().height() - 50, 80, 30)
        self.button.setGeometry(self.viewport().width() - 130, self.viewport().height() - 50, 130, 30)
        self.count_label.setGeometry(self.viewport().width() - 110, 10, 100, 30)
        self.dijkstra_button.setGeometry(self.viewport().width() - 130, self.viewport().height() - 100, 130, 30)

    def node_clicked(self, node_id):
        if node_id in self.G:
            node_info = self.G.nodes[node_id]
            print(f"Node {node_id} clicked. Node Information: {node_info}")

    def on_button_clicked(self):
        if len(self.selected_nodes) != 2:
            # Afficher un pop-up si moins ou plus de deux nœuds sont sélectionnés
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Sélection Incomplète")
            msg.setInformativeText("Veuillez sélectionner exactement deux nœuds pour lancer l'algorithme.")
            msg.setWindowTitle("Erreur")
            msg.exec_()
        else:
            N1 = self.selected_nodes[0].node_id
            N2 = self.selected_nodes[1].node_id
            # Demander le nombre d'itérations
            numIterations, okPressed = QInputDialog.getInt(self, "Nombre d'itérations","Combien d'itérations voulez-vous exécuter ?", 50, 1, 1000,1)

            if okPressed:
                self.algorithm_thread = AlgorithmThread(self.G, N1, N2, numIterations)  # Passer numIterations au thread
                self.algorithm_thread.count_updated.connect(self.update_count_label)
                self.algorithm_thread.conductivity_updated.connect(self.update_edges_in_bulk)
                self.algorithm_thread.finished_signal.connect(self.update_edges_display)
                self.algorithm_thread.time_elapsed_signal.connect(self.display_time_elapsed)
                self.algorithm_thread.start()

    def on_dijkstra_button_clicked(self):
        if len(self.selected_nodes) != 2:
            QMessageBox.warning(self, "Sélection Incomplète",
                                "Veuillez sélectionner exactement deux nœuds pour exécuter l'algorithme de Dijkstra.")
        else:
            start_node = self.selected_nodes[0].node_id
            end_node = self.selected_nodes[1].node_id

            try:
                # Spécifiez l'attribut 'length' comme poids pour l'algorithme de Dijkstra
                path = nx.dijkstra_path(self.G, start_node, end_node, weight='length')
                length = nx.dijkstra_path_length(self.G, start_node, end_node, weight='length')
                QMessageBox.information(self, "Résultat Dijkstra", f"Chemin: {path}\nLongueur: {length}")

                path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                self.update_edges_display(path_edges=path_edges)  # Passer seulement path_edges
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'exécution de Dijkstra: {e}")

    def update_time_label(self):
        if self.start_time is not None:
            elapsed_time = time.perf_counter() - self.start_time
            self.time_label.setText(f"Temps écoulé: {elapsed_time:.2f} sec")
            self.time_label.adjustSize()

    def on_algorithm_finished(self, selected_edges):
        self.timer.stop()

    def update_count_label(self, count):

        self.count_label.setText(f"Count: {count + 1}")

    def display_time_elapsed(self, elapsed_time):
        print(f"Temps écoulé : {elapsed_time:.2f} secondes.")
        # Ici, vous pouvez mettre à jour un QLabel ou tout autre widget pour afficher le temps

    def update_edges_display(self, selected_edges=None, path_edges=None):
        # Supprimer toutes les arêtes existantes
        for item in self.scene.items():
            if isinstance(item, QGraphicsLineItem):
                self.scene.removeItem(item)

        # Redessiner les arêtes avec la nouvelle coloration
        scale = 10000
        for edge in self.G.edges():
            source_node = self.G.nodes[edge[0]]
            target_node = self.G.nodes[edge[1]]
            line = QGraphicsLineItem(source_node['x'] * scale, -source_node['y'] * scale,
                                     target_node['x'] * scale, -target_node['y'] * scale)

            pen = QPen(Qt.green)  # Couleur par défaut pour les arêtes non sélectionnées
            pen.setWidth(0)  # Taille par défaut des arêtes

            # Si l'arête est dans les arêtes sélectionnées par Physarum, la colorier en rouge
            if selected_edges and (edge in selected_edges or (edge[1], edge[0]) in selected_edges):
                pen.setColor(Qt.red)

            # Si l'arête fait partie du chemin de Dijkstra, la colorier en bleu
            if path_edges and (edge in path_edges or (edge[1], edge[0]) in path_edges):
                pen.setColor(Qt.blue)
                pen.setWidth(2)  # Rendre les arêtes du chemin plus visibles

            line.setPen(pen)
            self.scene.addItem(line)

    def update_edges_in_bulk(self, conductivities):
        # Normaliser les conductivités ici
        max_conductivity = max(conductivities.values())
        min_conductivity = min(conductivities.values())

        # Préparer les modifications : calculer les nouvelles couleurs ou opacités
        updates = {}
        for edge, conductivity in conductivities.items():
            normalized_conductivity = ((conductivity - min_conductivity) /
                                       (
                                                   max_conductivity - min_conductivity)) if max_conductivity > min_conductivity else 1
            new_color = QColor(255, 0, 0, int(255 * normalized_conductivity))  # Exemple avec opacité ajustée
            updates[edge] = new_color


        # Appliquer les mises à jour en parcourant tous les éléments une seule fois
        for item in self.scene.items():
            if isinstance(item, QGraphicsLineItem):
                edge_id = item.data(0)
                if edge_id in updates:
                    pen = item.pen()
                    pen.setColor(updates[edge_id])
                    item.setPen(pen)

    def find_line_item_for_edge(self, edge):
        for item in self.scene.items():
            if isinstance(item, QGraphicsLineItem):
                edge_id = item.data(0)
                if edge_id == edge or edge_id == (edge[1], edge[0]):
                    return item
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isPanning = True
            self._panStartX = event.x()
            self._panStartY = event.y()
            self.setCursor(Qt.ClosedHandCursor)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._isPanning:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self._panStartX))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self._panStartY))
            self._panStartX = event.x()
            self._panStartY = event.y()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isPanning = False
            self.setCursor(Qt.ArrowCursor)

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoomLevel += 1
        else:
            zoomFactor = self.zoomOutFactor
            self.zoomLevel -= 1

        # Appliquer les limites de zoom
        if self.zoomLevel < self.zoomRange[0]: self.zoomLevel, zoomFactor = self.zoomRange[0], 1
        if self.zoomLevel > self.zoomRange[1]: self.zoomLevel, zoomFactor = self.zoomRange[1], 1

        self.scale(zoomFactor, zoomFactor)