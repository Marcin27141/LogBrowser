from PySide6.QtWidgets import QWidget, QMainWindow, QWidget
from View.ApplicationLayout import ApplicationLayout

class LogsAppMainWindow(QMainWindow):
    MAIN_WINDOW_TITLE = 'Log browser'
    def __init__(self, controller):
        super().__init__()
        self.setWindowTitle(self.MAIN_WINDOW_TITLE)
        widget = QWidget()
        widget.setLayout(ApplicationLayout(controller))
        self.setCentralWidget(widget)