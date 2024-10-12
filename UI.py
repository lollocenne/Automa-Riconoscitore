import sys
from PyQt5.QtWidgets import *
from scene import QGMGraphicsScene


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Automa Riconoscitore")
        
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.scene = QGMGraphicsScene()
        
        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)
        
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())