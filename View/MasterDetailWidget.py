from PySide6.QtWidgets import QWidget, QHBoxLayout, QWidget
from View.LogsQListWidget import LogsQListWidget
from View.DisplayLogDetailsWidget import DisplayLogDetailsWidget

class MasterDetailWidget(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.master = LogsQListWidget(controller)
        self.detail = DisplayLogDetailsWidget(controller)
        self.master.itemClicked.connect(self.on_master_item_click)
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(self.master)
        widget_layout.addWidget(self.detail)
        self.setLayout(widget_layout)

    def clear(self):
        self.master.clear()
        self.detail.clear_details()

    def initialize_list(self, filepath):
        self.master.initialize_list(filepath)
        self.detail.clear_details()

    def filter(self, predicate):
        self.master.filter(predicate)
        self.detail.clear_details()

    def reset_filters(self):
        self.master.reset_filters()
        self.detail.clear_details()
        
    def on_master_item_click(self, item):
        log = item.data(self.controller.LOG_DATA_ROLE)
        self.detail.display_details(log)