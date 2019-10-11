from typing import Type, List
from alert import Alert, AlertState
from logline import LogLine
import time

class Alerter:
    def __init__(self, alert_check_interval: int = 120, high_traffic_threshold: int = 10):
        self.last_alert: Alert = None
        self.alert_check_interval = alert_check_interval
        self.high_traffic_threshold = high_traffic_threshold

    def check_if_alert(self, recent_loglines: List[Type[LogLine]]):
        requests_per_second = len(recent_loglines) / self.alert_check_interval

        # Create a HIGH_TRAFFIC alert if there is no previous alert or it is of type RECOVERED
        # and the req/s is above the threshold
        if requests_per_second > self.high_traffic_threshold and not self._in_alert():
            self.last_alert = self._create_alert(AlertState.HIGH_TRAFFIC)
        # Create a RECOVERED alert if the current alert is HIGH_TRAFFIC and the req/s has dropped below the threshold
        elif requests_per_second <= self.high_traffic_threshold and self._in_alert():
            self.last_alert = self._create_alert(AlertState.RECOVERED)
    
    def get_alert(self) -> Type[Alert]:
        return self.last_alert

    def _in_alert(self):
        return self.last_alert and self.last_alert.state == AlertState.HIGH_TRAFFIC

    def _create_alert(self, state: Type[AlertState]) -> Type[Alert]:
        return Alert(state)
