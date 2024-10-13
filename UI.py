import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from scene import QGMGraphicsScene

from main import AutomaRiconoscitore
from nodo import Nodo


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.initUI()
        
        self.nodi = self.creaNodi(["ABAB"], ["A", "B"])
    
    def creaNodi(self, sequenze: list[str] = [], caratteri: list[str] = []) -> dict[str, dict[str, Nodo]]:
        modello = AutomaRiconoscitore(sequenze, caratteri)
        modello.creaNodiAutoma()
        
        nodi = {}
        for key, value in modello.nodi.items():
            nodi[key] = Nodo(0, key, value, self.scene.addEllipse, (3500, 2000, QPen(Qt.black), QBrush(QColor.fromRgbF(.15,.15,.15)), QGraphicsItem.ItemIsMovable))
        return nodi
    
    def initUI(self):
        self.setWindowTitle("Automa Riconoscitore")
        
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.scene = QGMGraphicsScene()
        
        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)
        
        self.showMaximized()
        
        self.showNodes()
    
    def showNodes(self):
        ...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())