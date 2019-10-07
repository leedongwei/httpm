import time
import re

class LogLine:
    def __init__(self, host: str = None, authuser: str = None, date: int = None, request: str = None, status: int = None, _bytes: int = None):
        self.host = host
        self.authuser = authuser
        self.date = int(date) if date else None
        self.time = time.time()
        self.request = request
        self.status = int(status) if status else None
        self.bytes = int(_bytes) if _bytes else None

    @classmethod
    def from_line(cls, line: str):
        host, _, authuser, date, request, status, _bytes = line.split(",")
        return LogLine(host, authuser, date, request.replace('"', ''), status, _bytes)

    def get_section(self):
        match = re.match(r'\w+\s(\/\w+[\w\-\.]+)[\/\w+[\w\-\.\/]+]*\s.*', self.request).groups()
        return match[0]