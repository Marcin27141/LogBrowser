from PySide6.QtWidgets import QGroupBox, QVBoxLayout
from View.FilterWidgets import UserFilter, IpAddressFilter, FromDateFilter, ToDateFilter

class FiltersGroupBox(QGroupBox):
    def __init__(self, controller):
        super().__init__("Filters")
        self.filters = [UserFilter(), IpAddressFilter(), FromDateFilter(controller), ToDateFilter(controller)]
        widget_layout = QVBoxLayout()
        for filter in self.filters:
            widget_layout.addWidget(filter)
        self.setLayout(widget_layout)

    def clear(self):
        for filter in self.filters:
            filter.clear_value()

    def get_filters_predicates(self):
        return [_filter for _filter in self.filters if _filter.get_predicate() != None]