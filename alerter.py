from typing import Type, List
from alert import Alert, AlertState
from logline import LogLine

class Alerter:
    def __init__(self, alert_check_interval: int = 120, high_traffic_threshold: int = 10):
        self.last_alert: Alert = None
        self.alert_check_interval = alert_check_interval
        self.high_traffic_threshold = high_traffic_threshold

    def check_if_alert(self, recent_loglines: List[Type[LogLine]]) -> bool:
        requests_per_second = len(recent_loglines) / self.alert_check_interval

        # Create a HIGH_TRAFFIC alert if there is no previous alert or it is of type HIGH_TRAFFIC
        # and the req/s is above the threshold
        if not self.last_alert or self.last_alert.state == AlertState.RECOVERED:
            if requests_per_second > self.high_traffic_threshold:
                self.last_alert = self._create_alert(AlertState.HIGH_TRAFFIC)
                return True
        # Create a RECOVERED alert if the current alert is HIGH_TRAFFIC and the req/s has dropped below the threshold
        elif self.last_alert and self.last_alert.state == AlertState.HIGH_TRAFFIC:
            if requests_per_second <= self.high_traffic_threshold:
                self.last_alert = self._create_alert(AlertState.RECOVERED)
                return True
        
        return False

    def get_alert(self) -> Type[Alert]:
        return self.last_alert

    def _create_alert(self, state: Type[AlertState]):
        return Alert(state)
