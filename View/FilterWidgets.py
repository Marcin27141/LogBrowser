from View.TitleInputWidget import TitleInputWidget

class FromDateFilter(TitleInputWidget):
    def __init__(self, controller):
        super().__init__("From")
        self.controller = controller

    def get_predicate(self):
        if (from_date := self.controller.try_parse_date(self.value.text())):
            return (lambda log: from_date < log.log_tuple.date)
        else:
            return None

class ToDateFilter(TitleInputWidget):
    def __init__(self, controller):
        super().__init__("To")
        self.controller = controller

    def get_predicate(self):
        if (to_date := self.controller.try_parse_date(self.value.text())):
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
