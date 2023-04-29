
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QListWidgetItem, QListWidget, QPushButton, QLineEdit, QLabel, QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout, QFormLayout, QWidget
import sys
import Controller

LOG_DATA_ROLE = 100

class TitleValueWidget(QWidget):
    def __init__(self, title) -> None:
        super().__init__()
        self.title = QLabel(title)
        self.value = QLabel()
        self.title.setMinimumWidth(100)
        self.value.setMinimumWidth(125)
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(self.title)
        widget_layout.addWidget(self.value)
        self.setLayout(widget_layout)
    
    def update_value(self, new_value):
        self.value.setText(str(new_value))

    def clear_value(self):
        self.value.clear()

class TitleInputWidget(QWidget):
    def __init__(self, title) -> None:
        super().__init__()
        self.title = QLabel(title)
        self.value = QLineEdit()
        self.title.setMinimumWidth(100)
        self.value.setMinimumWidth(125)
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(self.title)
        widget_layout.addWidget(self.value)
        self.setLayout(widget_layout)

    def clear_value(self):
        self.value.clear()

class FromDateFilter(TitleInputWidget):
    def __init__(self):
        super().__init__("From")

    def get_predicate(self):
        if (from_date := Controller.try_parse_date(self.value.text())):
            return (lambda log: from_date < log.log_tuple.date)
        else:
            return lambda log: True

class ToDateFilter(TitleInputWidget):
    def __init__(self):
        super().__init__("To")

    def get_predicate(self):
        if (to_date := Controller.try_parse_date(self.value.text())):
            return (lambda log: log.log_tuple.date < to_date)
        else:
            return lambda log: True

class UserFilter(TitleInputWidget):
    def __init__(self):
        super().__init__("Username")

    def get_predicate(self):
        return (lambda log: log.username == self.value.text()) if self.value.text() else lambda log: True

class FiltersGroupBox(QGroupBox):
    def __init__(self):
        super().__init__("Filters")
        self.filters = [FromDateFilter(), ToDateFilter(), UserFilter()]
        widget_layout = QVBoxLayout()
        for filter in self.filters:
            widget_layout.addWidget(filter)
        self.setLayout(widget_layout)

    def get_filters_predicates(self):
        return [_filter.get_predicate() for _filter in self.filters]

class FiltersGroupWidget(QWidget):
    def __init__(self, logs_list_component):
        super().__init__()
        self.logs_list_component = logs_list_component
        self.filters_box = FiltersGroupBox()
        self.expand_filters_button = QPushButton('Expand Filters')
        self.filter_button = QPushButton('Filter')
        self.expand_filters_button.clicked.connect(self.toggle_filters)
        self.filter_button.clicked.connect(self.filter_logs)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.expand_filters_button)
        buttons_layout.addWidget(self.filter_button)
        widget_layout = QVBoxLayout()
        widget_layout.addLayout(buttons_layout)
        widget_layout.addWidget(self.filters_box)
        #widget_layout.setContentsMargins(30,0,0,0)
        self.setLayout(widget_layout)
        #self.setMaximumWidth(400)

    def toggle_filters(self):
        if self.filters_box.isVisible():
            self.filters_box.hide()
            self.expand_filters_button.setText('Show Filters')
        else:
            self.filters_box.show()
            self.expand_filters_button.setText('Hide Filters')

    def filter_logs(self):
        self.logs_list_component.filter(self.filters_box.get_filters_predicates())


class OpenFileWidget(QWidget):
    def __init__(self, logs_list_component) -> None:
        super().__init__()
        self.logs_list_component = logs_list_component
        self.filepath_input = QLineEdit()
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.button_clicked)
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(self.filepath_input)
        widget_layout.addWidget(self.open_button)
        self.setLayout(widget_layout)

    def button_clicked(self):
        filepath = self.filepath_input.text()
        if not Controller.check_if_file_exists(filepath):
            self.filepath_input.setText("File doesn't exist")
            self.logs_list_component.clear()
        else:
            self.logs_list_component.initialize_list(filepath)

class DisplayLogDetailsWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.user_display = TitleValueWidget("User")
        self.ip_display = TitleValueWidget("IP Address")
        self.date_display = TitleValueWidget("Date")
        self.pid_display = TitleValueWidget("PID")
        
        widget_layout = QVBoxLayout()
        widget_layout.addWidget(self.user_display)
        widget_layout.addWidget(self.ip_display)
        widget_layout.addWidget(self.date_display)
        widget_layout.addWidget(self.pid_display)
        self.setLayout(widget_layout)
    
    def display_details(self, log):
        self.user_display.update_value(log.username)
        self.ip_display.update_value(log.ip_addresses[0] if log.ip_addresses else None)
        self.date_display.update_value(log.log_tuple.date)
        self.pid_display.update_value(log.log_tuple.pid)

    def clear_details(self):
        self.user_display.clear_value()
        self.ip_display.clear_value()
        self.date_display.clear_value()
        self.pid_display.clear_value()


class LogsQListWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumWidth(400)

class MasterDetailWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.original_logs = None
        self.current_logs = None
        self.master = LogsQListWidget()
        self.detail = DisplayLogDetailsWidget()
        self.master.itemClicked.connect(self.on_master_item_click)
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(self.master)
        widget_layout.addWidget(self.detail)
        self.setLayout(widget_layout)

    def populate_list(self):
        for log in self.current_logs:
            list_widget = QListWidgetItem(str(log), self.master)
            list_widget.setData(LOG_DATA_ROLE, log)

    def initialize_list(self, filepath):
        self.clear()
        self.original_logs = Controller.read_all_logs(filepath)
        self.current_logs = self.original_logs
        self.populate_list()

    def clear(self):
        self.master.clearSelection()
        self.master.clear()
        self.detail.clear_details()

    def filter(self, predicate):
        if self.original_logs:
            self.clear()
            self.current_logs = Controller.filter_logs(self.original_logs, predicate)
            self.populate_list()
        
    def on_master_item_click(self, item):
        log = item.data(LOG_DATA_ROLE)
        self.detail.display_details(log)

class MasterDetailWithButtonsWidget(MasterDetailWidget):
    def __init__(self) -> None:
        super().__init__()
        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.previous_button, 0, alignment=Qt.AlignLeft)
        buttons_layout.addWidget(self.next_button, 0, alignment=Qt.AlignRight)
        """buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)"""
        new_layout = QVBoxLayout()
        super_widget = QWidget()
        super_widget.setLayout(super().layout())
        new_layout.addWidget(super_widget)
        #new_layout.addWidget(buttons_widget)
        #new_layout.addLayout(super().layout())
        new_layout.addLayout(buttons_layout)
        self.setLayout(new_layout)
        self.next_button.clicked.connect(self.select_next_item)
        self.previous_button.clicked.connect(self.select_previous_item)
        self.master.currentRowChanged.connect(self.on_current_row_changed)

    def reset_buttons(self):
        self.next_button.setEnabled(False)
        self.previous_button.setEnabled(False)

    def populate_list(self):
        super().populate_list()
        self.reset_buttons()

    def on_current_row_changed(self, row):
        item = self.master.item(row)
        if (item is not None):
            super().on_master_item_click(item)
            self.next_button.setEnabled(True) if row < self.master.count() - 1 else self.next_button.setEnabled(False)
            self.previous_button.setEnabled(True) if row > 0 else self.previous_button.setEnabled(False)

    def on_master_item_click(self, item):
        pass
        
    def select_next_item(self):
        if self.master.currentRow() < self.master.count():
            self.master.setCurrentRow(self.master.currentRow() + 1)

    def select_previous_item(self):
        if self.master.currentRow() > 0:
            self.master.setCurrentRow(self.master.currentRow() - 1)

class ApplicationLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.master_detail = MasterDetailWithButtonsWidget()
        self.file_opener = OpenFileWidget(self.master_detail)
        self.filter_widget = FiltersGroupWidget(self.master_detail)
        self.addWidget(self.file_opener)
        self.addWidget(self.filter_widget)
        self.addWidget(self.master_detail)

class LogsAppMainWindow(QMainWindow):
    MAIN_WINDOW_TITLE = 'Log browser'
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