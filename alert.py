from enum import Enum
from typing import Type
import time as t

class AlertState(Enum):
    RECOVERED = 0
    HIGH_TRAFFIC = 1

class Alert:
    def __init__(self, state: Type[AlertState], hits = None, time: float = t.localtime()):
        self.state = state
        self.time = time
        self.hits = hits

    def __str__(self):
        if self.state == AlertState.RECOVERED:
            return 'Alert recovered at {}'.format(t.strftime("%B %d, %Y, %H:%M:%S", self.time))
        elif self.state == AlertState.HIGH_TRAFFIC:
            return 'Hight traffic generated an alert - hits = {}, triggered at {}'.format(self.hits, t.strftime("%B %d, %Y, %H:%M:%S", self.time))
