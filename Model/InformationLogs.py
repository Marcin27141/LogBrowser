from Model.BaseLogClass import SSHLogEntry

class SSHInformationLog(SSHLogEntry):
    def __init__(self, line):
        super().__init__(line)

    def validate(self):
        return super().validate()