from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MiniWindow():
    def __init__(self, window, tipo: list[str]):
        self.tipo = tipo    #sequenze o caratteri
        
        self.finestra = QFrame(window)
        self.finestra.setFrameShape(QFrame.StyledPanel)
        self.finestra.setFixedHeight(50)
        
        self.finestra.setStyleSheet("""
            background-color: rgb(50, 50, 50);
            padding: 3px;
            color: white;
        """)
        
        self.layoutFinestra = QHBoxLayout()
        self.layoutFinestra.setAlignment(Qt.AlignLeft)
        self.finestra.setLayout(self.layoutFinestra)
    
    def aggiungiLabel(self, testo):
        label = QLabel(testo, self.finestra)
        
        label.setFixedWidth(len(testo)*8)
        label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);
        """)
        
        self.layoutFinestra.addWidget(label)
    
    def aggiungiBottone(self, testo):
        bottone = QPushButton(testo, self.finestra)
        bottone.clicked.connect(lambda: self.bottonePremuto(bottone, testo, self.tipo))
        
        self.layoutFinestra.addWidget(bottone)
    
    @staticmethod
    def bottonePremuto(bottone, testo: str, tipo: list[str]):
        tipo.remove(testo)
        bottone.deleteLater()
    
    def getayout(self):
        return self.finestra