from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnnAI Application")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        label = QLabel("Welcome to AnnAI!")
        layout.addWidget(label)
        
        self.setLayout(layout)