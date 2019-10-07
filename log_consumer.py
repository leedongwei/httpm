import time
from typing import Type
from pygtail import Pygtail

from logline import LogLine
from logkeep import LogKeep

class LogConsumer:
    def __init__(self, logkeep: Type[LogKeep]):
        self.logkeep = logkeep
        self._consuming = False

    def consume_log_file(self, file: str):
        self._consuming = True
        while self._consuming:
            try:
                for line in Pygtail(file):
                    print(line)
                    self.logkeep.add_logline(LogLine.from_line(line))
            except KeyboardInterrupt:
                raise
            time.sleep(0.250)

    def _stop(self):
        self._consuming = False