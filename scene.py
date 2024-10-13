from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class QGMGraphicsScene(QGraphicsScene):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.width, self.height = 4000, 2000
        self.setSceneRect(self.width//2, self.height//2, self.width, self.height)
        
        self.setBackgroundBrush(QColor("#404040"))
        
        self.pen1 = QPen(QColor("#2f2f2f"))
        self.pen1.setWidth(1)
        self.pen2 = QPen(QColor("#303030"))
        self.pen2.setWidth(2)
        
        self.greedSize = 20
    
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        
        right = int(math.floor(rect.right()))
        left = int(math.floor(rect.left()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))
        
        firtsLeft = left - left % self.greedSize
        firtsTop = top - top % self.greedSize
        
        lines1, lines2 = [], []
        for x in range(firtsLeft, right, self.greedSize):
            if x % 100 == 0:
                lines2.append(QLine(x, top, x, bottom))
            else:
                lines1.append(QLine(x, top, x, bottom))
        
        for y in range(firtsTop, bottom, self.greedSize):
            if y % 100 == 0:
                lines2.append(QLine(left, y, right, y))
            else:
                lines1.append(QLine(left, y, right, y))
        
        painter.setPen(self.pen1)
        painter.drawLines(*lines1)
        
        painter.setPen(self.pen2)
        painter.drawLines(*lines2)