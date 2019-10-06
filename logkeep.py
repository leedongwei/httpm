import time
class LogKeep:
    def __init__(self):
        self.recent_loglines = []
    
    def add_logline(self, log_line):
        self.recent_loglines += [log_line]

    def read_recent_loglines(self, from_last_n_seconds = 10):
        return [log_line for log_line in self.recent_loglines if time.time() - log_line.time < from_last_n_seconds]