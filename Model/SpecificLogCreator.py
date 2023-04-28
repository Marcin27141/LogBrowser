import Model.BaseLogClass
import Model.ErrorLogs
import Model.InformationLogs
import Model.PasswordAcceptedLogs
import Model.PasswordFailedLogs

class SpecificLogCreator:
    BASE_LOG_TYPE = Model.BaseLogClass.SSHLogEntry
    LAST_RESORT_LOG_TYPE = Model.InformationLogs.SSHInformationLog

    @staticmethod
    def is_abstract(_class):
        return bool(getattr(_class, "__abstractmethods__", False))
    
    def get_all_concrete_subclassess(self, _class):
        all_children_recursive = set(_class.__subclasses__()).union([sub for cl in _class.__subclasses__() for sub in self.get_all_concrete_subclassess(cl)])
        return [_subclass for _subclass in all_children_recursive if not SpecificLogCreator.is_abstract(_subclass)]

    def create_log(self, log_line) -> BASE_LOG_TYPE:
        for subclass in self.get_all_concrete_subclassess(self.BASE_LOG_TYPE):
            if subclass != self.LAST_RESORT_LOG_TYPE and (test_instance := subclass(log_line)).validate():
                return test_instance
        if self.LAST_RESORT_LOG_TYPE != None and (last_resort := self.LAST_RESORT_LOG_TYPE(log_line)).validate():
            return last_resort