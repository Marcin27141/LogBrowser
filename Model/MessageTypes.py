from enum import Enum

class MessageType(Enum):
    LOGIN_SUCCESSFUL = 1
    LOGIN_FAILED = 2
    CONNECTION_CLOSED = 3
    WRONG_PASSWORD = 4
    INVALID_USER = 5
    BREAK_IN_ATTEMPT = 6
    OTHER = 0