from PySide6.QtWidgets import QListWidget, QListWidgetItem

class LogsQListWidget(QListWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.all_chunks_loaded = False
        self.all_logs = None
        self.filtered_logs = None
        self.last_filter = None
        self.verticalScrollBar().valueChanged.connect(self.add_logs_if_needed)
        self.setMinimumWidth(400)

    def add_logs_if_needed(self, value):
        not_enough_for_scrollbar = self.verticalScrollBar().maximum() == 0
        reached_end_of_scrollbar = self.verticalScrollBar().maximum() == value
        if (not_enough_for_scrollbar or  reached_end_of_scrollbar) and not self.all_chunks_loaded:
            new_logs = self.controller.read_chunk_of_logs(self.filepath)
            if len(new_logs) == 0: self.all_chunks_loaded = True
            self.all_logs.merge(new_logs)
            if self.filtered_logs != None:
                new_logs = self.controller.filter_logs(new_logs, self.last_filter)
                self.filtered_logs.merge(new_logs)
            self.populate_list(new_logs)
            
    def initialize_list(self, filepath):
        self.reset_widget()
        self.filepath = filepath
        self.all_logs = self.controller.get_first_chunk_of_logs(filepath)
        self.populate_list(self.all_logs)

    def populate_list(self, logs):
        for log in logs:
            list_widget = QListWidgetItem(str(log), self)
            list_widget.setData(self.controller.LOG_DATA_ROLE, log)
        self.doItemsLayout()
        self.add_logs_if_needed(-1)

    def filter(self, predicate):
        if self.all_logs:
            self.last_filter = predicate
            self.clear()
            self.filtered_logs = self.controller.filter_logs(self.all_logs, predicate)
            self.populate_list(self.filtered_logs)

    def reset_filters(self):
        if self.filtered_logs:
            self.clear()
            self.filtered_logs = None
            self.populate_list(self.all_logs)

    def reset_widget(self):
        self.filtered_logs = None
        self.last_filter = None
        self.all_chunks_loaded = False
        self.clear()

    def clear(self):
        super().clear()
        self.scrollToTop()
        self.clearSelection()
        
