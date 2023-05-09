from PySide6.QtWidgets import QListWidget, QListWidgetItem
from View.FilterWidgets import FromDateFilter, ToDateFilter

class LogsQListWidget(QListWidget):
    LOADED_CHUNK_SIZE = 100
    
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.all_chunks_loaded = False
        self.all_logs = None
        self.filtered_logs = None
        self.last_filter = None
        self.num_of_loaded_and_displayed = 0
        self.verticalScrollBar().valueChanged.connect(self.add_logs_if_needed)
        self.setMinimumWidth(400)

    """def add_logs_if_needed(self, value):
        not_enough_for_scrollbar = self.verticalScrollBar().maximum() == 0
        reached_end_of_scrollbar = self.verticalScrollBar().maximum() == value
        if (not_enough_for_scrollbar or  reached_end_of_scrollbar) and not self.all_chunks_loaded:
            new_logs = self.controller.read_chunk_of_logs(self.filepath)
            if len(new_logs) == 0: self.all_chunks_loaded = True
            self.all_logs.merge(new_logs)
            if self.filtered_logs != None:
                new_logs = self.controller.filter_logs(new_logs, self.last_filter)
                self.filtered_logs.merge(new_logs)
            self.populate_list(new_logs)"""
    
    def add_logs_if_needed(self, value):
        displayed_logs = self.filtered_logs if self.filtered_logs != None else self.all_logs
        not_enough_for_scrollbar = self.verticalScrollBar().maximum() == 0
        reached_end_of_scrollbar = self.verticalScrollBar().maximum() == value
        displaying_loaded_logs = self.num_of_loaded_and_displayed < len(displayed_logs)
        if displaying_loaded_logs and (not_enough_for_scrollbar or  reached_end_of_scrollbar):
            self.add_next_chunk_of_loaded_logs(displayed_logs)
        elif (not_enough_for_scrollbar or  reached_end_of_scrollbar) and not self.all_chunks_loaded:
            self.load_next_chunk_of_logs()

    def add_next_chunk_of_loaded_logs(self, displayed_logs):
        upper = min(len(displayed_logs), self.num_of_loaded_and_displayed + self.LOADED_CHUNK_SIZE)
        new_logs = displayed_logs[self.num_of_loaded_and_displayed:upper]
        self.populate_list(new_logs)

    def load_next_chunk_of_logs(self):
        if not self.all_chunks_loaded:
            new_logs = self.controller.read_chunk_of_logs(self.filepath)
            if len(new_logs) == 0: self.all_chunks_loaded = True
            self.all_logs.merge(new_logs)
            if self.filtered_logs != None:
                new_logs = self.controller.filter_logs(new_logs, self.last_filter)
                print(type(self.last_filter[0]))
                if len(new_logs) > 0: self.filtered_logs.merge(new_logs)
                elif all(isinstance(filter, (FromDateFilter.get_predicate, ToDateFilter.get_predicate)) for filter in self.last_filter):
                    self.load_next_chunk_of_logs()
            self.populate_list(new_logs)
            
    def initialize_list(self, filepath):
        self.reset_widget()
        self.filepath = filepath
        self.all_logs = self.controller.get_first_chunk_of_logs(filepath)
        self.populate_list(self.all_logs)

    def populate_list(self, logs):
        upper = min(len(logs), self.LOADED_CHUNK_SIZE)
        for log_idx in range(upper):
            list_widget = QListWidgetItem(str(logs[log_idx]), self)
            list_widget.setData(self.controller.LOG_DATA_ROLE, logs[log_idx])
        self.num_of_loaded_and_displayed += upper
        self.doItemsLayout()
        self.add_logs_if_needed(-1)

    def filter(self, predicate):
        if self.all_logs:
            self.last_filter = predicate
            self.clear()
            self.num_of_loaded_and_displayed = 0
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
        self.num_of_loaded_and_displayed = 0
        self.clear()

    def clear(self):
        super().clear()
        self.scrollToTop()
        self.clearSelection()
        
