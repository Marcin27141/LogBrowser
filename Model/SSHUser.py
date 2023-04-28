import re

class SSHUser:
    USERNAME_PATTERN =  r"^[a-z_][a-z0-9_-]{0,31}$"

    def __init__(self, username):
        self.username = str(username or '')
        self.last_logged = None

    def __str__(self):
        return self.username

    def update_last_login_date(self, date):
        self.last_logged = date

    def validate(self):
        return bool(re.search(self.USERNAME_PATTERN, self.username))