from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QGraphicsEllipseItem, QApplication
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


class ClickableNode(QObject):
    clicked = pyqtSignal(int)

    def __init__(self, x, y, w, h, node_id, parent=None):
        super().__init__(parent)
        self.graphics_item = QGraphicsEllipseItem(x, y, w, h)
        self.graphics_item.setBrush(QBrush(Qt.white))  # Appliquer le pinceau au graphics_item

        # Définir un stylo transparent pour enlever la bordure
        transparent_pen = QPen(Qt.NoPen)  # Qt.NoPen crée un stylo "invisible"
        self.graphics_item.setPen(transparent_pen)

        # Conserver la taille originale pour l'animation de clic
        self.original_rect = self.graphics_item.rect()

        # Rendre l'élément graphique cliquable
        self.graphics_item.setAcceptHoverEvents(True)
        self.graphics_item.setAcceptedMouseButtons(Qt.LeftButton)

        # Référencer l'ID du nœud
        self.node_id = node_id

        self.is_selected = False

        # Associer les événements de la souris avec les méthodes de cette classe
        self.graphics_item.hoverEnterEvent = self.hoverEnterEvent
        self.graphics_item.hoverLeaveEvent = self.hoverLeaveEvent
        self.graphics_item.mousePressEvent = self.mousePressEvent
        self.graphics_item.mouseReleaseEvent = self.mouseReleaseEvent

    def hoverEnterEvent(self, event):
        QApplication.instance().setOverrideCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.instance().restoreOverrideCursor()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Réduire la taille du nœud pour simuler un clic
            shrink_factor = 0.9
            new_rect = self.original_rect.adjusted(
                self.original_rect.width() * (1 - shrink_factor) / 2,
                self.original_rect.height() * (1 - shrink_factor) / 2,
                -self.original_rect.width() * (1 - shrink_factor) / 2,
                -self.original_rect.height() * (1 - shrink_factor) / 2
            )
            self.graphics_item.setRect(new_rect)

            # Inverse l'état de sélection du nœud
            self.is_selected = not self.is_selected

            if self.is_selected:
                if len(self.parent().selected_nodes) < 2:
                    # Ajoute ce nœud à la liste des nœuds sélectionnés
                    self.parent().selected_nodes.append(self)
                    self.graphics_item.setBrush(QBrush(Qt.red))
                else:
                    # Retire le premier nœud sélectionné de la liste et le désélectionne
                    node_to_deselect = self.parent().selected_nodes.pop(0)
                    node_to_deselect.is_selected = False
                    node_to_deselect.graphics_item.setBrush(QBrush(Qt.white))

                    # Ajoute ce nœud à la liste
                    self.parent().selected_nodes.append(self)
                    self.graphics_item.setBrush(QBrush(Qt.red))
            else:
                # Le nœud a été désélectionné, le retirer de la liste
                self.parent().selected_nodes.remove(self)
                self.graphics_item.setBrush(QBrush(Qt.white))

            self.graphics_item.update()  # Mettre à jour l'affichage du nœud
            self.clicked.emit(self.node_id)  # Émettre le signal de clic

    def mouseReleaseEvent(self, event):
        # Revenir à la taille originale
        self.graphics_item.setRect(self.original_rect)