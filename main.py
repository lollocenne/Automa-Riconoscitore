import sys
import math

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtGui import QPainterPath, QPen, QBrush, QColor, QFont, QPolygonF
from PyQt5.QtCore import QPointF

from scene import QGMGraphicsScene
from view import QGMGraphicsView
from automaRiconoscitore import AutomaRiconoscitore
from nodo import Nodo
from miniWindow import MiniWindow


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.nodi = self.creaNodi(["ABA", "BBA"], ["A", "B"])
        self.drawObjects()
        self.curveItems = []
        self.creaCollegamenti()
    
    def creaNodi(self, sequenze: list[str] = [], caratteri: list[str] = []) -> dict[str, Nodo]:        
        self.modello = AutomaRiconoscitore(sequenze, caratteri)
        self.modello.creaNodiAutoma()
        nodi: dict[str, Nodo] = {}
        for key, value in self.modello.nodi.items():
            nodi[key] = Nodo(0, key, value, self.scene, (4000, 2000), self)
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
        angolo = math.atan2(y1 - y2, x1 - x2)
        x2, y2 = nodo2.getBordo(angolo)
        
        path = QPainterPath(QPointF(x1, y1))
        
        if nodo1 is nodo2:
            offset = nodo1.diametro * 1.5
            ctrl = QPointF(x1, y1 - offset)
            path.quadTo(ctrl, QPointF(x1, y1))
        else:
            offset = math.dist((x1, y1), (x2, y2)) / 2
            
            if y1 < y2:
                ctrl = QPointF((x1 + x2) / 2, max(y1, y2) - offset)
            else:
                ctrl = QPointF((x1 + x2) / 2, min(y1, y2) + offset)
            
            path.quadTo(ctrl, QPointF(x2, y2))
        
        pen = QPen(QBrush(QColor("black")), 3)
        
        curva = self.scene.addPath(path, pen)
        curva.setZValue(0)
        
        pointMid = path.pointAtPercent(0.5)
        
        label = self.scene.addText(carattere, QFont("Arial", 12))
        label.setDefaultTextColor(QColor("white"))
        labelRect = label.boundingRect()
        
        if y1 < y2:
            label.setPos(pointMid.x() - labelRect.width() / 2, pointMid.y() + labelRect.height() / 2 - 10)
        else:
            label.setPos(pointMid.x() - labelRect.width() / 2, pointMid.y() - labelRect.height() / 2 - 10)
        
        grandezzaFreccia = 12
        if nodo1 is nodo2:
            xFreccia = x1
            yFreccia = y1 - nodo1.diametro / 2
            angoloFreccia = math.pi / 2
            frecciaP1 = QPointF(xFreccia + grandezzaFreccia * math.cos(angoloFreccia - math.pi / 6), yFreccia - grandezzaFreccia * math.sin(angoloFreccia - math.pi / 6))
            frecciaP2 = QPointF(xFreccia + grandezzaFreccia * math.cos(angoloFreccia + math.pi / 6), yFreccia - grandezzaFreccia * math.sin(angoloFreccia + math.pi / 6))
            punta = QPolygonF([QPointF(xFreccia, yFreccia), frecciaP1, frecciaP2])
            freccia = self.scene.addPolygon(punta, QPen(QColor("black")), QBrush(QColor("black")))
        else:
            pointBeforeEnd = path.pointAtPercent(0.98)
            angoloFreccia = math.atan2(y2 - pointBeforeEnd.y(), x2 - pointBeforeEnd.x()) + math.pi
            frecciaP1 = QPointF(x2 + grandezzaFreccia * math.cos(angoloFreccia - math.pi / 6), y2 + grandezzaFreccia * math.sin(angoloFreccia - math.pi / 6))
            frecciaP2 = QPointF(x2 + grandezzaFreccia * math.cos(angoloFreccia + math.pi / 6), y2 + grandezzaFreccia * math.sin(angoloFreccia + math.pi / 6))
            punta = QPolygonF([QPointF(x2, y2), frecciaP1, frecciaP2])
            freccia = self.scene.addPolygon(punta, QPen(QColor("black")), QBrush(QColor("black")))
        
        self.curveItems.append((curva, label, freccia))
    
    def clearCurves(self):
        for curva, label, freccia in self.curveItems:
            self.scene.removeItem(curva)
            self.scene.removeItem(label)
            self.scene.removeItem(freccia)
        self.curveItems.clear()
    
    def disegnaCreaAutomaBottone(self):
        def ricreaAutoma():
            self.scene.clear()
            Nodo.x = Nodo.fixedX
            Nodo.y = Nodo.fixedY
            self.nodi = self.creaNodi(self.modello.sequenze, self.modello.caratteri)
            self.curveItems = []
            self.creaCollegamenti()
        
        finestra = MiniWindow(self)
        finestra.aggiungiBottonePermanente("CREA AUTOMA", ricreaAutoma)
        
        self.layout.addWidget(finestra.getayout())
    
    def disegnaSequenzeInputs(self):
        finestra = MiniWindow(self, self.modello.sequenze)
        finestra.aggiungiLabel("Sequenza:")
        finestra.aggiungiTextBox("Scrivi Sequenza")
        for s in self.modello.sequenze:
            finestra.aggiungiBottone(s)
        
        self.layout.addWidget(finestra.getayout())
    
    def disegnaCaratteriInputs(self):
        finestra = MiniWindow(self, self.modello.caratteri)
        finestra.aggiungiLabel("Caratteri:")
        finestra.aggiungiTextBox("Scrivi Carattere")
        for c in self.modello.caratteri:
            finestra.aggiungiBottone(c)
        
        self.layout.addWidget(finestra.getayout())
    
    def initUI(self):
        self.setWindowTitle("Automa Riconoscitore")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.scene = QGMGraphicsScene()
        self.view = QGMGraphicsView(self.scene, self)
        
        self.layout.addWidget(self.view)
        self.showMaximized()
    
    def drawObjects(self):
        self.disegnaCreaAutomaBottone()
        self.disegnaSequenzeInputs()
        self.disegnaCaratteriInputs()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())