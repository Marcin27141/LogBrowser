from Model.LogJournal import SSHLogJournal
import os


def read_from_file(_func):
    def check_if_file_exists(path):
        return os.path.isfile(path)
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