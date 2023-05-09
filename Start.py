from PySide6.QtWidgets import QApplication
from View.LogsAppMainWindow import LogsAppMainWindow
from Controller import Controller
import sys

controller = Controller()
app = QApplication(sys.argv)
window = LogsAppMainWindow(controller)
window.show()
sys.exit(app.exec())