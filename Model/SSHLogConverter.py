from collections import namedtuple
import re
from datetime import datetime
import re

SSH_LOG_REGEX_STRING = r"(?P<date>[A-Z][a-z]{2}\s+\d{1,2} \d\d:\d\d:\d\d) (?P<host>\w+) (?P<component>\w+)\[(?P<pid>\d+)\]: (?P<description>.+)$"
SSH_LOG_REGEX = re.compile(SSH_LOG_REGEX_STRING, re.MULTILINE)
SSH_DATE_FORMAT = r"%b %d %H:%M:%S"

SSH_Log = namedtuple('LogTuple', ['date', 'host', 'component', 'pid', 'description'])

def convert_line_to_ssh_tuple(line):
    return None if not (match := SSH_LOG_REGEX.match(line)) else SSH_Log(
        date=datetime.strptime(match.group('date'), SSH_DATE_FORMAT),
        host=match.group('host'),
        component=match.group('component'),
        pid=int(match.group('pid')),
        description=match.group('description')
    )