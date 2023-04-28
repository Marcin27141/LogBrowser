from Model.BaseLogClass import SSHLogEntry
from abc import abstractmethod
import re

class SSHErrorLog(SSHLogEntry):  
    def __init__(self, log):
        super().__init__(log)
        self._error_match = None        

    @property
    @abstractmethod
    def error_type(self):
        pass

    @property
    @abstractmethod
    def error_description(self):
        pass

    def __eq__(self, other):
        return (super().__eq__(other) and
                isinstance(other, SSHErrorLog) and
                other.error_type == self.error_type and
                other.error_description == self.error_description)
    
    def validate(self):
        return super().validate() and bool(self._error_match)
    

class ExceptionErrorLog(SSHErrorLog):
    EXCEPTION_ERROR_CODE = 3
    EXCEPTION_ERROR_PATTERN = r"^error: Received disconnect from (?:[0-9]{1,3}\.){3}[0-9]{1,3}: 3: (?P<exception>(?:\w|\.)+): (?P<description>.*) \[preauth\]$"

    def __init__(self, log):
        super().__init__(log)
        self._error_match = self._try_match_ssh_tuple_description(self.EXCEPTION_ERROR_PATTERN)
        self.__error_description = self.__get_error_description()

    def __get_error_description(self):
        return f'{re.try_get_group(self._error_match, "exception")}: {re.try_get_group(self._error_match, "description")}'

    @property
    def error_type(self):
        return self.EXCEPTION_ERROR_CODE

    @property
    def error_description(self):
        return self.__error_description
    

class DisconectedByUserErrorLog(SSHErrorLog):
    DISCONECTED_BY_USER_ERROR_CODE = 13
    DISCONNECTED_BY_USER_ERROR_PATTERN = r"^error: Received disconnect from (?:[0-9]{1,3}\.){3}[0-9]{1,3}: 13: (?P<description>.*) \[preauth\]$"

    def __init__(self, log):
        super().__init__(log)
        self._error_match = self._try_match_ssh_tuple_description(self.DISCONNECTED_BY_USER_ERROR_PATTERN)
        self.__error_description = self.__get_error_description()

    def __get_error_description(self):
        return re.try_get_group(self._error_match, "description")

    @property
    def error_type(self):
        return self.DISCONECTED_BY_USER_ERROR_CODE

    @property
    def error_description(self):
        return self.__error_description
    

class NoMoreAuthMethodsErrorLog(SSHErrorLog):
    NO_MORE_AUTH_METHODS_ERROR_CODE = 14
    NO_MORE_AUTH_METHODS_ERROR_PATTERN = r"^error: Received disconnect from (?:[0-9]{1,3}\.){3}[0-9]{1,3}: 14: (?P<description>.*) \[preauth\]$"

    def __init__(self, log):
        super().__init__(log)
        self._error_match = self._try_match_ssh_tuple_description(self.NO_MORE_AUTH_METHODS_ERROR_PATTERN)
        self.__error_description = self.__get_error_description()

    def __get_error_description(self):
        return re.try_get_group(self._error_match, "description")

    @property
    def error_type(self):
        return self.NO_MORE_AUTH_METHODS_ERROR_PATTERN

    @property
    def error_description(self):
        return self.__error_description
