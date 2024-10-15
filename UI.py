import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from scene import QGMGraphicsScene
from view import QGMGraphicsView
from main import AutomaRiconoscitore
from nodo import Nodo


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.nodi = self.creaNodi(["ABAB"], ["A", "B"])
        self.curveItems = []
        self.creaCollegamenti()

    def creaNodi(self, sequenze: list[str] = [], caratteri: list[str] = []) -> dict[str, Nodo]:
        modello = AutomaRiconoscitore(sequenze, caratteri)
        modello.creaNodiAutoma()
        nodi = {}
        for key, value in modello.nodi.items():
            nodo = Nodo(0, key, value, self.scene, (3500, 2000))
            nodo.showNode.setFlag(QGraphicsItem.ItemIsMovable, True)
            nodi[key] = nodo
        return nodi

    def creaCollegamenti(self):
        self.clearCurves()
        for nodo in self.nodi.values():
            for carattere, statoDest in nodo.puntaA.items():
                nodoDest = self.nodi.get(statoDest)
                if nodoDest:
                    self.disegnaCurva(nodo, nodoDest, carattere)

    def disegnaCurva(self, nodo1: Nodo, nodo2: Nodo, carattere: str):
        x1, y1 = nodo1.getCenter()
        x2, y2 = nodo2.getCenter()
        
        offset = 50
        path = QPainterPath(QPointF(x1, y1))
        ctrl1 = QPointF(x1 + 100, y1 - 100 + offset)
        ctrl2 = QPointF(x2 - 100, y2 - 100 - offset)
        
        path.cubicTo(ctrl1, ctrl2, QPointF(x2, y2))
        pen = QPen(Qt.black, 3)
        curva = self.scene.addPath(path, pen)
        
        midX = (x1 + x2) / 2
        midY = (y1 + y2) / 2
        
        label = self.scene.addText(carattere, QFont("Arial", 12))
        label.setPos(midX, midY - 20)
        self.curveItems.append((curva, label))

    def clearCurves(self):
        for curva, label in self.curveItems:
            self.scene.removeItem(curva)
            self.scene.removeItem(label)
        self.curveItems.clear()

    def initUI(self):
        self.setWindowTitle("Automa Riconoscitore")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.scene = QGMGraphicsScene()
        self.view = QGMGraphicsView(self.scene, self)
        
        self.layout.addWidget(self.view)
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())