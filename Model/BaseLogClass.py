from abc import ABC
import Model.RegexExtensions
from ipaddress import IPv4Address
from Model.SSHLogConverter import SSH_Log, convert_line_to_ssh_tuple
import re
class SSHLogEntry(ABC):
    def __init__(self, line):
        self._log_line = line
        self.username = None 
        self.ip_addresses = None

        self.log_tuple: SSH_Log = convert_line_to_ssh_tuple(line)
        if (self.log_tuple):
            self.username = self.__get_log_username()
            self.ip_addresses = self.__get_ip_addresses()

    def __str__(self) -> str:
        return self._log_line
    
    def __repr__(self):
        return f"{type(self).__name__}({self.log_tuple})"
    
    def __eq__(self, other):
        return (isinstance(other, SSHLogEntry) and
                other.log_tuple.date == self.log_tuple.date and
                other.log_tuple.host == self.log_tuple.host and
                other.log_tuple.pid == self.log_tuple.pid)
    
    def __lt__(self, other):
        return isinstance(other, SSHLogEntry) and self.log_tuple.date < other.log_tuple.date
    
    def __gt__(self, other):
        return isinstance(other, SSHLogEntry) and self.log_tuple.date > other.log_tuple.date
    
    def _try_match_ssh_tuple_description(self, pattern):
        return re.search(pattern, self.log_tuple.description) if self.log_tuple else None
    
    def __get_ip_addresses(self):
        IP_REGEX_STRING = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        ipv4s = list(re.findall(IP_REGEX_STRING, self.log_tuple.description))
        return [IPv4Address(ip_address) for ip_address in ipv4s]
    
    def __get_log_username(self):
        USER_REGEX_STRING = r"(?<=\suser\s)\S+"
        return _match.group() if (_match := re.search(USER_REGEX_STRING, self.log_tuple.description)) else None

    @property
    def has_ip(self):
        return self._ip_addresses != None and len(self._ip_addresses) > 0

    def validate(self):
        return self.log_tuple != None