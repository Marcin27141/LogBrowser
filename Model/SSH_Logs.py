import re

SSH_LOG_REGEX_STRING = r"(?P<date>[A-Z][a-z]{2}\s+\d{1,2} \d\d:\d\d:\d\d) (?P<host>\w+) (?P<component>\w+)\[(?P<pid>\d+)\]: (?P<description>.+)$"
SSH_LOG_REGEX = re.compile(SSH_LOG_REGEX_STRING, re.MULTILINE)
SSH_DATE_FORMAT = r"%b %d %H:%M:%S"