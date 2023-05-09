from Model.LogJournal import SSHLogJournal
from Model.SSH_Logs import SSH_DATE_FORMAT
import os
from datetime import datetime
from itertools import islice

class Controller:
    LOG_DATA_ROLE = 100

    def __init__(self):
        self.filepath = None
        self.lines_reader = None

    def check_if_file_exists(self, path):
        return os.path.isfile(path)

    def read_from_file(self, filepath):
        if self.check_if_file_exists(filepath):
            self.filepath = filepath
            with open(filepath, 'r') as logs:
                return logs

    def read_all_logs(self, filepath):
        contents = self.read_from_file(filepath)
        return SSHLogJournal(contents)
    
    def get_first_chunk_of_logs(self, filepath):
        if self.lines_reader and self.lines_reader.filepath == filepath:
            self.lines_reader.reset()
        else:
            self.lines_reader = LinesReader(filepath)
        return SSHLogJournal(self.lines_reader.read_chunk())
    
    def read_chunk_of_logs(self, filepath):
        if not self.lines_reader or self.lines_reader.filepath != filepath:
            self.lines_reader = LinesReader(filepath)
        return SSHLogJournal(self.lines_reader.read_chunk())

    def filter_logs(self, logs, predicates):
        filtered_logs = logs.filter(predicates)
        filtered_list = SSHLogJournal()
        filtered_list.set_logs(filtered_logs)
        return filtered_list
    
    def present_date_in_log_format(self, date):
        return date.strftime(SSH_DATE_FORMAT)
    
    def try_parse_date(self, date):
        try:
            return datetime.strptime(date, SSH_DATE_FORMAT)
        except ValueError:
            return None

class LinesReader:
    LINES_CHUNK = 100
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines_read = 0

    def check_if_file_exists(self, path):
        return os.path.isfile(path)

    def read_chunk(self):
        if self.check_if_file_exists(self.filepath):
            with open(self.filepath, 'r') as contents:
                result = [line.strip() for line in islice(contents, self.lines_read, self.lines_read + self.LINES_CHUNK)]
                self.lines_read += len(result)
                return result
            
    def reset(self):
        self.lines_read = 0
