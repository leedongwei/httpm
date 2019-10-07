from traffic_statistic import TrafficStatistic
from logline import LogLine
from typing import Type, Dict, List
import operator

class AverageRequestSizeStatistic(TrafficStatistic):
    def __init__(self, statistic_delay = 10):
        self.statistic_delay = statistic_delay
    
    def calculate_statistic(self, recent_loglines: List[Type[LogLine]]) -> None:
        avg_request_size = self._get_avg_request_size(recent_loglines)
        print('The average size of requests received in the last {} seconds is: {} bytes'.format(self.statistic_delay, avg_request_size))

    def _get_avg_request_size(self, recent_loglines: List[Type[LogLine]]) -> float:
        return sum([logline.bytes for logline in recent_loglines]) / len(recent_loglines)
