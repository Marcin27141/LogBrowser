from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout
from View.MasterDetailWithButtonsWidget import MasterDetailWithButtonsWidget
from View.OpenFileWidget import OpenFileWidget
from View.FiltersGroupWidget import FiltersGroupWidget

class ApplicationLayout(QVBoxLayout):
    def __init__(self, controller):
        super().__init__()
        self.master_detail = MasterDetailWithButtonsWidget(controller)
        self.file_opener = OpenFileWidget(controller, self.master_detail)
        self.filter_widget = FiltersGroupWidget(controller, self.master_detail)
        self.addWidget(self.file_opener)
        self.addWidget(self.filter_widget, 0, alignment=Qt.AlignHCenter)
        self.addWidget(self.master_detail)
