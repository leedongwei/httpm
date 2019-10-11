import time
class LogKeep:
    def __init__(self, keep_from_last_seconds: int = 10):
        self.recent_loglines = []
        self.keep_from_last_seconds = keep_from_last_seconds
    
    def add_logline(self, log_line):
        self.recent_loglines += [log_line]
        self.recent_loglines = [log_line for log_line in self.recent_loglines if time.time() - log_line.time < self.keep_from_last_seconds]

    def read_recent_loglines(self, from_last_n_seconds: int = 10):
        return [log_line for log_line in self.recent_loglines if time.time() - log_line.time < from_last_n_seconds]