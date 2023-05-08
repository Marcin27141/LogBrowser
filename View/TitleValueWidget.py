from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget

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