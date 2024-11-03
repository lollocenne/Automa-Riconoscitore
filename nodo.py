from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF

import math

#classe che rappresenta ogni nodo
#y: int -> la y del nodo
#stato: str -> indica lo stato del nodo, questo stato verrà mostrato all'utente
#puntaA: dict[str : str] -> dizionario che indica per ogni carattere possibile a quale stato bisogna collegare il nodo

#ogni nodo sarà salvato in un dizionario con lo stato come chiave e l'istanza come valore

class Nodo:
    fixedX = -300
    fixedY = 0
    x = fixedX
    y = fixedY
    
    def __init__(self, y: int = 0, stato: str = "", puntaA: dict[str, str] = {}, scene = None, coord: tuple[int] = (0, 0), finestra = None):
        self.x = Nodo.x + coord[0]
        self.y = Nodo.y + y + coord[1]
        
        self.diametro: int = 100        
        Nodo.x += self.diametro*2.5
        Nodo.y += 1
        
        self.stato = stato
        self.puntaA = puntaA    #{lettera : stato}
        
        self.finestra = finestra
        
        self.showNode = QGMGraphicsEllipseItem(QRectF(self.x, self.y, self.diametro, self.diametro),
                                                lambda: (self.finestra.creaCollegamenti(), self.drawState()))
        scene.addItem(self.showNode)
        
        self.textItem = QGraphicsTextItem(self.stato)
        font = QFont()
        font.setPointSize(10)
        self.textItem.setFont(font)
        self.textItem.setZValue(1)
        
        self.drawState()
        scene.addItem(self.textItem)

    def getCenter(self) -> tuple[int]:
        position = self.showNode.scenePos()
        
        centerX = position.x() + self.x + self.diametro / 2
        centerY = position.y() + self.y + self.diametro / 2
        return (centerX, centerY)
    
    def getBordo(self, angolo: float) -> tuple[int]:
        posx, posy = self.getCenter()
        raggio = self.diametro/2
        return (posx + raggio * math.cos(angolo), posy + raggio * math.sin(angolo))
    
    def drawState(self) -> None:
        position = self.showNode.scenePos()
        
        centerX = position.x() + self.x + self.diametro / 2 - self.textItem.boundingRect().width() / 2
        centerY = position.y() + self.y + self.diametro / 2 - self.textItem.boundingRect().height() / 2
        
        self.textItem.setPos(centerX, centerY)
        self.textItem.setDefaultTextColor(Qt.white)

#estensione di QGraphicsEllipseItem
class QGMGraphicsEllipseItem(QGraphicsEllipseItem):
    def __init__(self, rect, func):
        super().__init__(rect)
        self.setPen(QPen(Qt.black))
        self.setBrush(QBrush(QColor.fromRgbF(.15, .15, .15)))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setZValue(1)
        
        self.func = func

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.func()