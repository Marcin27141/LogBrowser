from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget

class OpenFileWidget(QWidget):
    def __init__(self, controller, logs_list_component) -> None:
        super().__init__()
        self.controller = controller
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
        if not self.controller.check_if_file_exists(filepath):
            self.filepath_input.setText("File doesn't exist")
        else:
            self.logs_list_component.initialize_list(filepath)