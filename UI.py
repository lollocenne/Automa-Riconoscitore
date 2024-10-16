import sys
import math

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
        self.nodi = self.creaNodi(["BBA", "ABA"], ["A", "B"])
        self.curveItems = []
        self.creaCollegamenti()

    def creaNodi(self, sequenze: list[str] = [], caratteri: list[str] = []) -> dict[str, Nodo]:
        modello = AutomaRiconoscitore(sequenze, caratteri)
        modello.creaNodiAutoma()
        nodi = {}
        for key, value in reversed(modello.nodi.items()):
            nodo = Nodo(0, key, value, self.scene, (4000, 2000))
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
        
        path = QPainterPath(QPointF(x1, y1))
        
        if nodo1 is nodo2:
            offset = nodo1.diametro * 1.5
            ctrl = QPointF(x1, y1 - offset)
            path.quadTo(ctrl, QPointF(x1, y1))
        else:
            offset = math.dist((x1, y1), (x2, y2)) / 2
            
            if x1 < x2 or y1 > y2:
                ctrl = QPointF((x1 + x2) / 2, max(y1, y2) + offset)
            else:
                ctrl = QPointF((x1 + x2) / 2, min(y1, y2) - offset)
            
            path.quadTo(ctrl, QPointF(x2, y2))
        
        gradient = QLinearGradient(QPointF(x1, y1), QPointF(x2, y2))
        gradient.setColorAt(0, QColor("red"))      #inizio
        gradient.setColorAt(1, QColor("black"))    #fine
        
        pen = QPen(QBrush(gradient), 3)
        
        curva = self.scene.addPath(path, pen)
        curva.setZValue(0)
        
        pointMid = path.pointAtPercent(0.5)
        
        label = self.scene.addText(carattere, QFont("Arial", 12))
        labelRect = label.boundingRect()
        
        if x1 < x2 or y1 > y2:
            label.setPos(pointMid.x() - labelRect.width() / 2, pointMid.y() + labelRect.height() / 2 - 10)
        else:
            label.setPos(pointMid.x() - labelRect.width() / 2, pointMid.y() - labelRect.height() / 2 - 10)
        
        self.curveItems.append((curva, label))

    def clearCurves(self):
        for curva, label in self.curveItems:
            self.scene.removeItem(curva)
            self.scene.removeItem(label)
        self.curveItems.clear()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.creaCollegamenti()
        return super().mousePressEvent(event)

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