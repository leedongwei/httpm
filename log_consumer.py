import time
from typing import Type
from pygtail import Pygtail
from logline import LogLine
from logkeep import LogKeep

class LogConsumer:
    def __init__(self, file: str, logkeep: Type[LogKeep]):
        self.pygtail = Pygtail(file, paranoid=True)
        self.logkeep = logkeep

    def consume_next_lines(self):
        while True:
            try:
                line = self.pygtail.next()
                if line:
                    self.logkeep.add_logline(LogLine.from_line(line))
            except StopIteration:
                break
