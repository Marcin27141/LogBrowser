from Model.BaseLogClass import SSHLogEntry
import re

class SSHPasswordAcceptedLog(SSHLogEntry):
    PASSWORD_ACCEPTED_PATTERN = r"^Accepted password for (?P<user>\w+) from (?:[0-9]{1,3}\.){3}[0-9]{1,3} port (?P<port>\d+) (?P<version>\w+)$"

    def __init__(self, log):
        super().__init__(log)
        self._log_match = self._try_match_ssh_tuple_description(self.PASSWORD_ACCEPTED_PATTERN)
        self.__subject_name = self.__get_user_name()
        self.__port_number = self.__get_port_number()
        self.__ssh_version = self.__get_ssh_version()

    def __get_user_name(self):
        return re.try_get_group(self._log_match, "user")
    
    def __get_port_number(self):
        return re.try_get_group(self._log_match, "port")
    
    def __get_ssh_version(self):
        return re.try_get_group(self._log_match, "version")

    @property
    def subject_name(self):
        return self.__subject_name

    @property
    def port_number(self):
        return self.__port_number

    @property
    def ssh_version(self):
        return self.__ssh_version

    def __eq__(self, other):
        return (super().__eq__(other) and
                isinstance(other, SSHPasswordAcceptedLog) and
                other.subject_name == self.subject_name and
                other.port_number == self.port_number and
                other.ssh_version == self.ssh_version)

    def validate(self):
        return super().validate() and bool(self._log_match)
    