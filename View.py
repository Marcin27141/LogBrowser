from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget
import sys
import Controller

LOG_DATA_ROLE = 100

logs = Controller.read_all_logs("test.txt")

class LogsQListWidget(QListWidget):
    def __init__(self, logs) -> None:
        super().__init__()
        self.populate_list(logs)

    def populate_list(self, logs):
        for log in logs:
            list_widget = QListWidgetItem(str(log), self)
            list_widget.setData(LOG_DATA_ROLE, log)

class ApplicationLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.data_label = QLabel()
        self.logs_list = LogsQListWidget(logs)
        self.logs_list.itemClicked.connect(self.on_list_item_click)
        self.addWidget(self.data_label)
        self.addWidget(self.logs_list)

    def on_list_item_click(self, item):
        log = item.data(LOG_DATA_ROLE)
        self.data_label.setText(f"date:{log.log_tuple.date}, pid:{log.log_tuple.pid}")

class LogsAppMainWindow(QMainWindow):
    MAIN_WINDOW_TITLE = 'Logs App'
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.MAIN_WINDOW_TITLE)
        widget = QWidget()
        widget.setLayout(ApplicationLayout())
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = LogsAppMainWindow()
window.show()
sys.exit(app.exec())