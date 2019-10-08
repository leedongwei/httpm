from enum import Enum
from typing import Type
import datetime

class AlertState(Enum):
    RECOVERED = 0
    HIGH_TRAFFIC = 1

class Alert:
    def __init__(self, state: Type[AlertState], hits = None):
        self.state = state
        self.time = datetime.datetime.now()
        self.hits = hits

    def __str__(self):
        if self.state == AlertState.RECOVERED:
            return 'Alert recovered at {}'.format(self.time)
        elif self.state == AlertState.HIGH_TRAFFIC:
            return 'Hight traffic generated an alert - hits = {}, triggered at time {}'.format(self.hits, self.time)
