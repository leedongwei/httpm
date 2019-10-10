from typing import Type, List
from logkeep import LogKeep
from alerter import Alerter
from traffic_statistic import TrafficStatistic

class HTTPLogMonitor:
    def __init__(self, logkeep: Type[LogKeep], alerter: Type[Alerter], traffic_stats: List[Type[TrafficStatistic]], stats_delay_interval: int = 10):
        self.logkeep = logkeep
        self.alerter = alerter
        self.stats_delay_interval = stats_delay_interval
        self.traffic_stats = traffic_stats

    def calculate_stats(self):
        recent_loglines = self.logkeep.read_recent_loglines(from_last_n_seconds=self.stats_delay_interval)
        for statistic in self.traffic_stats:
            statistic.calculate_statistic(recent_loglines)

    def has_alert(self) -> bool:
        recent_loglines = self.logkeep.read_recent_loglines(from_last_n_seconds=self.stats_delay_interval)
        return self.alerter.check_if_alert(recent_loglines)

    def get_alert(self):
        return self.alerter.get_alert()

