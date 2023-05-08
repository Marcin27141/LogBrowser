from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from View.MasterDetailWidget import MasterDetailWidget

class MasterDetailWithButtonsWidget(MasterDetailWidget):
    def __init__(self, controller) -> None:
        super().__init__(controller)
        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.previous_button, 0, alignment=Qt.AlignLeft)
        buttons_layout.addWidget(self.next_button, 0, alignment=Qt.AlignRight)
        new_layout = QVBoxLayout()
        super_widget = QWidget()
        super_widget.setLayout(super().layout())
        new_layout.addWidget(super_widget)
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