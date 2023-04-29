from Model.LogJournal import SSHLogJournal
from Model.SSH_Logs import SSH_DATE_FORMAT
import os
from datetime import datetime

def check_if_file_exists(path):
    return os.path.isfile(path)

def read_from_file(_func):
    def wrapper(filepath):
        if check_if_file_exists(filepath):
            with open(filepath, 'r') as logs:
                return _func(logs)
    return wrapper

@read_from_file
def read_all_logs(logs):
    log_journal = SSHLogJournal()
    for log_line in logs:
        log_journal.append(log_line)
    return log_journal

def filter_logs(logs, predicates):
    return logs.filter(predicates)

def try_parse_date(date):
    try:
        return datetime.strptime(date, SSH_DATE_FORMAT)
    except ValueError:
        return None