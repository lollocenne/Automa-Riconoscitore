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