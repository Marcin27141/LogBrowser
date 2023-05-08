from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel

class OpenFileWidget(QWidget):
    def __init__(self, controller, logs_list_component) -> None:
        super().__init__()
        self.controller = controller
        self.logs_list_component = logs_list_component
        self.filepath_input = QLineEdit()
        self.open_button = QPushButton("Open")
        self.not_found_label = QLabel()
        self.setLayout(self.get_widget_layout())
        self.open_button.clicked.connect(self.try_load_file)

    def get_widget_layout(self):
        widget_layout = QVBoxLayout()
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.filepath_input)
        upper_layout.addWidget(self.open_button)
        widget_layout.addLayout(upper_layout)
        widget_layout.addWidget(self.not_found_label)
        return widget_layout

    def try_load_file(self):
        filepath = self.filepath_input.text()
        if not self.controller.check_if_file_exists(filepath):
            self.not_found_label.setText("File not found")
        else:
            self.not_found_label.clear()
            self.logs_list_component.initialize_list(filepath)