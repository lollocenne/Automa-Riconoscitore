#classe che rappresenta ogni nodo
#y: int -> la y del nodo
#stato: str -> indica lo stato del nodo, questo stato verrà mostrato all'utente
#puntaA: dict[str : str] -> dizionario che indica per ogni carattere possibile a quale stato bisogna collegare il nodo

#ogni nodo sarà salvato in un dizionario con lo stato come chiave, e l'istanza come valore

from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt

class Nodo:
    x = -300
    y = 0
    def __init__(self, y: int = 0, stato: str = "", puntaA: dict[str, str] = {}, scene = None, coord: tuple[int] = (0, 0)):
        self.x = Nodo.x + coord[0]
        self.y = Nodo.y + y + coord[1]
        
        self.diametro: int = 100        
        Nodo.x += self.diametro*3
        Nodo.y += 1
        
        self.stato = stato if stato else "<finale>"
        self.puntaA = puntaA    #{lettera : stato}
        
        self.showNode = scene.addEllipse(self.x, self.y, self.diametro, self.diametro, QPen(Qt.black), QBrush(QColor.fromRgbF(.15, .15, .15)))
        self.showNode.setFlag(QGraphicsItem.ItemIsMovable)
        self.showNode.setZValue(1)
        
        
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
    
    def drawState(self):
        position = self.showNode.scenePos()
        
        centerX = position.x() + self.x + self.diametro / 2 - self.textItem.boundingRect().width() / 2
        centerY = position.y() + self.y + self.diametro / 2 - self.textItem.boundingRect().height() / 2
        
        self.textItem.setPos(centerX, centerY)
        self.textItem.setDefaultTextColor(Qt.white)