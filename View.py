from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget
import sys
import Controller

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Logs App')
LOG_DATA_ROLE = 100

def on_item_click(item):
    log = item.data(LOG_DATA_ROLE)
    data_label.setText(f"date:{log.log_tuple.date}, pid:{log.log_tuple.pid}")

logs = Controller.read_all_logs("test.txt")

class LogsQListWidget(QListWidget):
    def __init__(self, logs) -> None:
        super().__init__()
        self.populate_list(logs)
        self.itemClicked.connect(on_item_click)

    def populate_list(self, logs):
        for log in logs:
            list_widget = QListWidgetItem(str(log), self)
            list_widget.setData(LOG_DATA_ROLE, log)


_list = LogsQListWidget(logs)

layout = QVBoxLayout()
data_label = QLabel()
layout.addWidget(data_label)
layout.addWidget(_list)

widget = QWidget()
widget.setLayout(layout)
window.setCentralWidget(widget)

window.show()
sys.exit(app.exec())