
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QListWidgetItem, QListWidget, QPushButton, QLineEdit, QLabel, QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout, QFormLayout, QWidget
import sys
from Controller import Controller

LOG_DATA_ROLE = 100
global CONTROLLER
CONTROLLER = Controller()

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
        if (from_date := CONTROLLER.try_parse_date(self.value.text())):
            return (lambda log: from_date < log.log_tuple.date)
        else:
            return None

class ToDateFilter(TitleInputWidget):
    def __init__(self):
        super().__init__("To")

    def get_predicate(self):
        if (to_date := CONTROLLER.try_parse_date(self.value.text())):
            return (lambda log: log.log_tuple.date < to_date)
        else:
            return None

class UserFilter(TitleInputWidget):
    def __init__(self):
        super().__init__("Username")

    def get_predicate(self):
        return (lambda log: log.username == self.value.text()) if self.value.text() else None
    

class IpAddressFilter(TitleInputWidget):
    def __init__(self):
        super().__init__("IP address")

    def get_predicate(self):
        return (lambda log: log.ip_addresses and format(log.ip_addresses[0]) == self.value.text()) if self.value.text() else None

class FiltersGroupBox(QGroupBox):
    def __init__(self):
        super().__init__("Filters")
        self.filters = [UserFilter(), IpAddressFilter(), FromDateFilter(), ToDateFilter()]
        widget_layout = QVBoxLayout()
        for filter in self.filters:
            widget_layout.addWidget(filter)
        self.setLayout(widget_layout)

    def clear(self):
        for filter in self.filters:
            filter.clear_value()

    def get_filters_predicates(self):
        predicates = [_filter.get_predicate() for _filter in self.filters]
        return [predicate for predicate in predicates if predicate]

class FiltersGroupWidget(QWidget):
    def __init__(self, logs_list_component):
        super().__init__()
        self.logs_list_component = logs_list_component
        self.filters_box = FiltersGroupBox()
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
        #widget_layout.setContentsMargins(30,0,0,0)
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
        if not CONTROLLER.check_if_file_exists(filepath):
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
        self.ip_display.update_value(log.ip_addresses[0] if log.ip_addresses else "")
        self.date_display.update_value(CONTROLLER.present_date_in_log_format(log.log_tuple.date))
        self.pid_display.update_value(log.log_tuple.pid)

    def clear_details(self):
        self.user_display.clear_value()
        self.ip_display.clear_value()
        self.date_display.clear_value()
        self.pid_display.clear_value()


class LogsQListWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.all_logs = None
        self.filtered_logs = None
        self.verticalScrollBar().valueChanged.connect(self.add_logs_if_needed)
        self.setMinimumWidth(400)

    def add_logs_if_needed(self, value):
        if value == self.verticalScrollBar().maximum() and not self.filtered_logs:
            new_logs = CONTROLLER.read_chunk_of_logs(self.filepath)
            self.populate_list(new_logs)
            self.all_logs.merge(new_logs)

    def initialize_list(self, filepath):
        self.filepath = filepath
        self.clear()
        self.all_logs = CONTROLLER.get_first_chunk_of_logs(filepath)
        self.populate_list(self.all_logs)

    def populate_list(self, logs):
        for log in logs:
            list_widget = QListWidgetItem(str(log), self)
            list_widget.setData(LOG_DATA_ROLE, log)

    def filter(self, predicate):
        if self.all_logs:
            self.clear()
            self.filtered_logs = CONTROLLER.filter_logs(self.all_logs, predicate)
            self.populate_list(self.filtered_logs)

    def reset_filters(self):
        if self.filtered_logs:
            self.clear()
            self.filtered_logs = None
            self.populate_list(self.all_logs)

    def clear(self):
        self.scrollToTop()
        super().clear()
        self.clearSelection()
        

class MasterDetailWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.master = LogsQListWidget()
        self.detail = DisplayLogDetailsWidget()
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
        self.addWidget(self.filter_widget, 0, alignment=Qt.AlignHCenter)
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