from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

class ClickableButton(QPushButton):
    clicked_signal = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        # Quand le bouton est cliqué
        self.clicked_signal.emit()
        print("Bouton cliqué")

