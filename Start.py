from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from View.LogsAppMainWindow import LogsAppMainWindow
import sys
from Controller import Controller

controller = Controller()
app = QApplication(sys.argv)
window = LogsAppMainWindow(controller)
window.show()
sys.exit(app.exec())