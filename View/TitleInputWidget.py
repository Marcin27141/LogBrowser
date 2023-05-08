from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit

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