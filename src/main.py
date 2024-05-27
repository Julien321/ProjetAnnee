import sys
from PyQt5.QtWidgets import QApplication
from graph.graph_view import GraphView




def main():

    app = QApplication(sys.argv)
    view = GraphView()
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
