from Model.SpecificLogCreator import SpecificLogCreator
from datetime import datetime
from functools import reduce

class SSHLogJournal:
    SPECIFIC_LOG_CREATOR = SpecificLogCreator()

    def __init__(self, logs = []):
        self.logs = logs

    def __len__(self): return len(self.logs)

    def __iter__(self): return iter(self.logs)

    def __contains__(self, _log):
        return any(log == _log for log in self.logs)

    def __getitem__(self, idx):
        return self.logs[idx]
    
    def append(self, log_line):
        if (created_log := self.create_proper_log(log_line)):
            self.logs.append(created_log)

    def filter(self, predicates):
        predicate = reduce(lambda acc, predic: acc and predic, predicates)
        return [log for log in self.logs if predicate(log)]       

    def get_logs_between_dates(self, start, end):
        time_format = r"%d.%m %H:%M:%S"
        try:
            start_time = datetime.strptime(start, time_format)
            end_time = datetime.strptime(end, time_format)
            return [log for log in self.logs if start_time <= log.log_tuple.date <= end_time]
        except ValueError:
            print(f"Date format was incorrect. Correct format: {time_format}")

    @staticmethod
    def create_proper_log(log_line):
        return SSHLogJournal.SPECIFIC_LOG_CREATOR.create_log(log_line)
