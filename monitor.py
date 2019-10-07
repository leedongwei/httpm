from typing import Type, List
from logkeep import LogKeep
from traffic_statistic import TrafficStatistic

class HTTPLogMonitor:
    def __init__(self, logkeep: Type[LogKeep], alerter, traffic_stats: List[Type[TrafficStatistic]]):
        self.logkeep = logkeep
        self.alerter = alerter
        self.traffic_stats = traffic_stats

    def calculate_stats(self):
        recent_loglines = self.logkeep.read_recent_loglines()
        for statistic in self.traffic_stats:
            statistic.calculate_statistic(recent_loglines)

    def get_alert(self):
        pass