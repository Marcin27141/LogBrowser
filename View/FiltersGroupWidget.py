from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from View.FiltersGroupBox import FiltersGroupBox

class FiltersGroupWidget(QWidget):
    def __init__(self, controller, logs_list_component):
        super().__init__()
        self.logs_list_component = logs_list_component
        self.filters_box = FiltersGroupBox(controller)
        self.filters_box.hide()
        self.clear_filters_button = QPushButton('Clear Filters')
        self.expand_filters_button = QPushButton('Show Filters')
        self.filter_button = QPushButton('Filter')
        self.clear_filters_button.clicked.connect(self.clear_filters)
        self.expand_filters_button.clicked.connect(self.toggle_filters)
        self.filter_button.clicked.connect(self.filter_logs)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.clear_filters_button)
        buttons_layout.addWidget(self.expand_filters_button)
        buttons_layout.addWidget(self.filter_button)
        widget_layout = QVBoxLayout()
        widget_layout.addLayout(buttons_layout)
        widget_layout.addWidget(self.filters_box)
        self.setLayout(widget_layout)
        self.setMinimumWidth(400)

    def clear_filters(self):
        self.filters_box.clear()
        self.logs_list_component.reset_filters()

    def toggle_filters(self):
        if self.filters_box.isVisible():
            self.filters_box.hide()
            self.expand_filters_button.setText('Show Filters')
        else:
            self.filters_box.show()
            self.expand_filters_button.setText('Hide Filters')

    def filter_logs(self):
        filters = self.filters_box.get_filters_predicates()
        self.logs_list_component.filter(filters) if len(filters) > 0 else self.logs_list_component.reset_filters()