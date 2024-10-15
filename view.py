from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QGMGraphicsView(QGraphicsView):    
    def __init__(self, scene, parent = None):
        super().__init__(parent)
        
        self.scene = scene
        
        self.initUI()
        
        self.setScene(self.scene)
    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)
        
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)
    
    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)