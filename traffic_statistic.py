import abc
from typing import Type, List
from logline import LogLine

class TrafficStatistic(abc.ABC):
    @abc.abstractmethod
    def calculate_statistic(self, recent_loglines: List[Type[LogLine]]) -> None:
        pass
