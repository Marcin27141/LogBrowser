from PySide6.QtWidgets import QVBoxLayout, QWidget
from View.TitleValueWidget import TitleValueWidget

class DisplayLogDetailsWidget(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
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
        self.user_display.update_value(log.username if log.username else "")
        self.ip_display.update_value(log.ip_addresses[0] if log.ip_addresses else "")
        self.date_display.update_value(self.controller.present_date_in_log_format(log.log_tuple.date))
        self.pid_display.update_value(log.log_tuple.pid)

    def clear_details(self):
        self.user_display.clear_value()
        self.ip_display.clear_value()
        self.date_display.clear_value()
        self.pid_display.clear_value()