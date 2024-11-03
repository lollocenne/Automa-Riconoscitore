from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QLineEdit
from PyQt5.QtCore import Qt
from nodoAutoma import NodoAutoma


class MiniWindow():
    def __init__(self, window, tipo: list[str] = []):
        self.tipo = tipo    #sequenze o caratteri
        
        self.finestra = QFrame(window)
        self.finestra.setFrameShape(QFrame.StyledPanel)
        self.finestra.setFixedHeight(60)
        
        self.finestra.setStyleSheet("""
            background-color: rgb(50, 50, 50);
            padding: 3px;
            color: white;
        """)
        
        self.layoutFinestra = QHBoxLayout()
        self.layoutFinestra.setAlignment(Qt.AlignLeft)
        self.finestra.setLayout(self.layoutFinestra)
    
    def aggiungiLabel(self, testo) -> None:
        label = QLabel(testo, self.finestra)
        
        label.setFixedWidth(len(testo)*8)
        label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 50);
        """)
        
        self.layoutFinestra.addWidget(label)
    
    def aggiungiBottone(self, testo = "", func = None) -> None:
        bottone = QPushButton(testo, self.finestra)
        bottone.setFixedHeight(self.finestra.height()//2)
        bottone.setFixedWidth(bottone.fontMetrics().boundingRect(bottone.text()).width() + 20)
        bottone.clicked.connect(lambda: self.bottonePremuto(bottone, testo, self.tipo, func))
        
        self.layoutFinestra.addWidget(bottone)
    
    def aggiungiBottonePermanente(self, testo = "", func = None) -> None:
        bottone = QPushButton(testo, self.finestra)
        bottone.setFixedHeight(self.finestra.height()//2)
        bottone.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        bottone.clicked.connect(lambda: (func(), setattr(NodoAutoma, 'stato', 0)))
        
        self.layoutFinestra.addWidget(bottone)
    
    @staticmethod
    def bottonePremuto(bottone, testo: str, tipo: list[str], func) -> None:
        if func:
            func()
        
        try:
            tipo.remove(testo)
        except ValueError:
            pass
        
        bottone.deleteLater()
    
    def aggiungiTextBox(self, testo: str) -> None:
        self.textBox = QLineEdit(self.finestra)
        self.textBox.setPlaceholderText(testo)
        self.textBox.setFixedWidth(200)
        self.textBox.returnPressed.connect(lambda: self.aggiungiInput())
        
        self.layoutFinestra.addWidget(self.textBox)
    
    def aggiungiInput(self) -> None:
        input = self.textBox.text()
        
        if not input: return
        
        self.aggiungiBottone(input)
        self.tipo.append(input)
        self.textBox.clear()
    
    def getayout(self):
        return self.finestra