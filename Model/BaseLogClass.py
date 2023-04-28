from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from Model.Lab5_1 import SSH_Log
import Model.Lab5_1
import Model.RegexExtensions
import re
class SSHLogEntry(ABC):
    def __init__(self, line):
        self._log_line = line
        self.username = None 
        self.ip_addresses = None

        self.log_tuple: SSH_Log = Model.Lab5_1.convert_line_to_ssh_tuple(line)
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
        return [IPv4Address(ip_address) for ip_address in Model.Lab5_1.get_ipv4s_from_log(self.log_tuple)]
    
    def __get_log_username(self):
        return Model.Lab5_1.get_user_from_log(self.log_tuple)

    @property
    def has_ip(self):
        return self._ip_addresses != None and len(self._ip_addresses) > 0

    def validate(self):
        return self.log_tuple != None


"""myLog = SSHLogInformation("Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186")
myLog2 = SSHLogInformation("Dec 12 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186")
print(myLog == myLog2)
print(myLog < myLog2)
print(myLog > myLog2)"""
"""fail_log = SSHLogPasswordFailed("Dec 10 07:27:55 LabSZ sshd[24237]: Failed password for root from 112.95.230.3 port 47068 ssh2")
print(fail_log)
print(fail_log.log_tuple)
print(fail_log.get_ip_addresses())
print(fail_log.validate("Dec 10 07:27:55 LabSZ sshd[24237]: Failed password for root from 112.95.230.3 port 47068 ssh2"))"""