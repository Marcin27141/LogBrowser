from Model.BaseLogClass import SSHLogEntry
from abc import abstractmethod
import re

class SSHPasswordFailedLog(SSHLogEntry):  
    def __init__(self, log):
        super().__init__(log)
        self._log_match = None  

    @property
    @abstractmethod
    def subject_type(self):
        pass

    @property
    @abstractmethod
    def subject_name(self):
        pass

    @property
    @abstractmethod
    def port_number(self):
        pass

    @property
    @abstractmethod
    def ssh_version(self):
        pass

    def __eq__(self, other):
        return (super().__eq__(other) and
                isinstance(other, SSHPasswordFailedLog) and
                other.subject_type == self.subject_type and
                other.subject_name == self.subject_name and
                other.port_number == self.port_number and
                other.ssh_version == self.ssh_version)
    
    def validate(self):
        return super().validate() and bool(self._log_match)
    


class PasswordFailedForRoot(SSHPasswordFailedLog):
    FAILED_FOR_ROOT_CODE = 0
    ROOT_FAILED_PATTERN = r"^Failed password for (?P<root>root) from (?:[0-9]{1,3}\.){3}[0-9]{1,3} port (?P<port>\d+) (?P<version>\w+)$"

    def __init__(self, log):
        super().__init__(log)
        self._log_match = self._try_match_ssh_tuple_description(self.ROOT_FAILED_PATTERN)
        self.__subject_name = self.__get_root_name()
        self.__port_number = self.__get_port_number()
        self.__ssh_version = self.__get_ssh_version()

    def __get_root_name(self):
        return re.try_get_group(self._log_match, "root")
    
    def __get_port_number(self):
        return re.try_get_group(self._log_match, "port")
    
    def __get_ssh_version(self):
        return re.try_get_group(self._log_match, "version")

    @property
    def subject_type(self):
        return self.FAILED_FOR_ROOT_CODE

    @property
    def subject_name(self):
        return self.__subject_name

    @property
    def port_number(self):
        return self.__port_number

    @property
    def ssh_version(self):
        return self.__ssh_version


class PasswordFailedForUser(SSHPasswordFailedLog):
    FAILED_FOR_USER_CODE = 1
    USER_FAILED_PATTERN = r"^Failed password for invalid user (?P<user>\w+) from (?:[0-9]{1,3}\.){3}[0-9]{1,3} port (?P<port>\d+) (?P<version>\w+)$"

    def __init__(self, log):
        super().__init__(log)
        self._log_match = self._try_match_ssh_tuple_description(self.USER_FAILED_PATTERN)
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
    def subject_type(self):
        return self.FAILED_FOR_USER_CODE

    @property
    def subject_name(self):
        return self.__subject_name

    @property
    def port_number(self):
        return self.__port_number

    @property
    def ssh_version(self):
        return self.__ssh_version


class PasswordFailedForService(SSHPasswordFailedLog):
    FAILED_FOR_SERVICE_CODE = 2
    SERVICE_FAILED_PATTERN = r"^Failed password for (?P<service>\w+) (?<!root\s)from (?:[0-9]{1,3}\.){3}[0-9]{1,3} port (?P<port>\d+) (?P<version>\w+)$"

    def __init__(self, log):
        super().__init__(log)
        self._log_match = self._try_match_ssh_tuple_description(self.SERVICE_FAILED_PATTERN)
        self.__subject_name = self.__get_service_name()
        self.__port_number = self.__get_port_number()
        self.__ssh_version = self.__get_ssh_version()

    def __get_service_name(self):
        return re.try_get_group(self._log_match, "service")
    
    def __get_port_number(self):
        return re.try_get_group(self._log_match, "port")
    
    def __get_ssh_version(self):
        return re.try_get_group(self._log_match, "version")
        
    @property
    def subject_type(self):
        return self.FAILED_FOR_SERVICE_CODE

    @property
    def subject_name(self):
        return self.__subject_name

    @property
    def port_number(self):
        return self.__port_number

    @property
    def ssh_version(self):
        return self.__ssh_version
