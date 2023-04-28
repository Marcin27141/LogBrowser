from collections import namedtuple
import re
from datetime import datetime
from random import sample
import random
import statistics
from Model.SSH_Logs import SSH_LOG_REGEX, SSH_DATE_FORMAT
from Model.MessageTypes import MessageType

SSH_Log = namedtuple('LogTuple', ['date', 'host', 'component', 'pid', 'description'])

MESSAGE_TYPES_DICT = {
    MessageType.LOGIN_SUCCESSFUL: r"^Accepted password for .+",
    MessageType.LOGIN_FAILED: r".+authentication failure.+",
    MessageType.CONNECTION_CLOSED: r"^Connection closed by .+",
    MessageType.WRONG_PASSWORD: r"^Failed password for .+",
    MessageType.INVALID_USER: r"^Invalid user .+",
    MessageType.BREAK_IN_ATTEMPT: r".+POSSIBLE BREAK-IN ATTEMPT!$",
    }

def convert_line_to_ssh_tuple(line):
    #LoggingModule.log_bytes_read(count_bytes_in_string(line))
    return None if not (match := SSH_LOG_REGEX.match(line)) else SSH_Log(
        date=datetime.strptime(match.group('date'), SSH_DATE_FORMAT),
        host=match.group('host'),
        component=match.group('component'),
        pid=int(match.group('pid')),
        description=match.group('description')
    )

def convert_ssh_tuple_to_line(_tuple: SSH_Log):
    return f"{_tuple.date.strftime(SSH_DATE_FORMAT)} {_tuple.host} {_tuple.component}[{_tuple.pid}]: {_tuple.description}"

def convert_text_to_tuples_list(text):
    return [ssh_tuple for line in text if (ssh_tuple := convert_line_to_ssh_tuple(line))]

def count_bytes_in_string(text):
    ENCODING_SYSTEM = 'utf-8'
    return len(text.encode(ENCODING_SYSTEM))

def get_ipv4s_from_log(ssh_tuple: SSH_Log):
    IP_REGEX_STRING = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
    return list(re.findall(IP_REGEX_STRING, ssh_tuple.description))

def get_user_from_log(ssh_tuple: SSH_Log):
    USER_REGEX_STRING = r"(?<=\suser\s)\S+"
    return _match.group() if (_match := re.search(USER_REGEX_STRING, ssh_tuple.description)) else None

def get_message_type(description):
    for key, type in MESSAGE_TYPES_DICT.items():
        if re.search(type, description):
            #LoggingModule.handle_message_type_logging(key, description)
            return key
    return MessageType.OTHER

def get_random_user_logs(text, num_of_logs: int = 5):
    if num_of_logs <= 0: raise ValueError("Number of logs must be at least 1")

    def populate_users_logs_dict(_logs, _dict):
        for line in _logs:
            if (ssh_tuple := convert_line_to_ssh_tuple(line)) and (user := get_user_from_log(ssh_tuple)):
                _dict.setdefault(user, []).append(line)
        
    users_logs = {}
    populate_users_logs_dict(text, users_logs)
    random_user = random.choice(list(users_logs.keys()))
    
    try: 
        return sample(users_logs[random_user], num_of_logs)
    except ValueError:
            print(f"User {random_user} doesn't have enough logs ({len(users_logs[random_user])} available, {num_of_logs} requested)")

def get_ssh_duration_statistics(text, each_user_separate = False):
    
    def get_updated_session_data(old_data, new_latest, new_user):
        old_start, old_latest, old_user = old_data
        updated_user = new_user if old_user == None and new_user != None else old_user
        return (old_start, new_latest, updated_user)

    def just_determined_session_user(old_user, new_user):
        return old_user == None and new_user != None

    def get_sessions_beginnings_and_ends(_text, with_users):
        sessions_dict = {}  #(date, pid): (session_start, session_end, session_user)
        users_sessions = {} #user: (list:(date,pid))
        for line in _text:
            if ssh_tuple := convert_line_to_ssh_tuple(line):
                _user = get_user_from_log(ssh_tuple)
                _logtime = ssh_tuple.date
                _key = (ssh_tuple.pid, _logtime.date())
                if _key not in sessions_dict:
                    sessions_dict[_key] = (_logtime, _logtime, _user)
                    if with_users and _user != None: users_sessions.setdefault(_user, []).append(_key)
                else:
                    if with_users and just_determined_session_user(sessions_dict[_key][2], _user):
                        users_sessions.setdefault(_user, []).append(_key)
                    sessions_dict[_key] = get_updated_session_data(sessions_dict[_key], _logtime, _user)
        return sessions_dict, users_sessions
    
    def get_session_duration(start, end):
        return int((end - start).total_seconds())
    
    def get_sessions_durations(sessions_dict, sessions_list):
        return [get_session_duration(sessions_dict[key][0], sessions_dict[key][1]) for key in sessions_list]
    
    def get_user_sessions_statistics(user_and_sessions):
        return (user_and_sessions[0], statistics.mean(user_and_sessions[1]), statistics.pstdev(user_and_sessions[1]))
    

    sessions_dict, users_sessions_dict = get_sessions_beginnings_and_ends(text, each_user_separate)
    if each_user_separate:
        users_sessions_durations = [(user, get_sessions_durations(sessions_dict, keys_list)) for user, keys_list in users_sessions_dict.items()]
        return list(map(lambda user_and_sessions: get_user_sessions_statistics(user_and_sessions), users_sessions_durations))
    else:
        sessions_durations = [get_session_duration(start, end) for (start, end, user) in sessions_dict.values()]
        return statistics.mean(sessions_durations), statistics.pstdev(sessions_durations)


def get_users_login_counts(text):
    
    def get_user_if_password_accepted(description):
        SSH_LOGIN_REGEX = r"(?<=Accepted password for\s)\w+"
        return _match.group() if (_match := re.search(SSH_LOGIN_REGEX, description)) else None
    
    users_logs_count = {}

    for line in text:
        if (ssh_tuple := convert_line_to_ssh_tuple(line)) and (user := get_user_if_password_accepted(ssh_tuple.description)):
            users_logs_count.setdefault(user, 0)
            users_logs_count[user] += 1
    return users_logs_count

def get_rarest_and_most_frequent_users(text, num_of_rarest: int = 5, num_of_most_frequent: int = 5):
    if num_of_rarest < 0 or num_of_most_frequent < 0: raise ValueError("Number of users can't be negative")

    users_login_counts = get_users_login_counts(text)
    sorted_users_by_logs_counts = sorted(users_login_counts.items(), key=lambda kvp: kvp[1])
    _min = sorted_users_by_logs_counts[:num_of_rarest]
    _max = sorted_users_by_logs_counts[-num_of_most_frequent:]
    return (_min, _max)

def get_rarest_and_most_frequent_user(text):
    users_login_counts = get_users_login_counts(text)
    _min = min(users_login_counts, key=users_login_counts.get)
    _max = max(users_login_counts, key=users_login_counts.get)
    return ((_min, users_login_counts[_min]), (_max, users_login_counts[_max]))