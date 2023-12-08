from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsLineItem
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt
from src.gui.clickable_node import ClickableNode
import networkx as nx
from .graph_loader import load_graph
from functools import partial

class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(Qt.black)  # Fond noir
        self.setScene(self.scene)
        self.setRenderHints(QPainter.Antialiasing)

        self.G = None
        self.init_graph_view()

        self.zoomInFactor = 1.25  # Facteur de zoom avant
        self.zoomOutFactor = 1 / self.zoomInFactor  # Facteur de zoom arrière
        self.zoomRange = [0, 10]  # Limites de zoom [min, max]
        self.zoomLevel = 0  # Niveau de zoom actuel

        self.setDragMode(QGraphicsView.ScrollHandDrag)  # Optionnel pour l'effet visuel

        self._isPanning = False
        self._panStartX = 0
        self._panStartY = 0

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

    def init_graph_view(self):
        self.G = load_graph("data/BRU.json")
        scale = 10000
        pen = QPen(Qt.green)
        pen.setWidth(0)

        for node_id in self.G.nodes():
            node_data = self.G.nodes[node_id]
            node_item = ClickableNode(node_data['x'] * scale, -node_data['y'] * scale, 2.5, 2.5, node_id)
            node_item.clicked.connect(partial(self.node_clicked, node_id))
            self.scene.addItem(node_item.graphics_item)



        for edge in self.G.edges():
            source_node = self.G.nodes[edge[0]]
            target_node = self.G.nodes[edge[1]]
            line = QGraphicsLineItem(source_node['x'] * scale, -source_node['y'] * scale,
                                     target_node['x'] * scale, -target_node['y'] * scale)
            line.setPen(pen)
            self.scene.addItem(line)

        # Méthode pour gérer le clic sur un nœud

    def node_clicked(self, node_id):
        if node_id in self.G:
            node_info = self.G.nodes[node_id]
            print(f"Node {node_id} clicked")
            print("Node Information:", node_info)
        else:
            print(f"Node {node_id} does not exist in the graph.")
