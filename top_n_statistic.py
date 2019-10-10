from traffic_statistic import TrafficStatistic
from logline import LogLine
from typing import Type, Dict, List, Tuple, Any
import abc
import operator
import heapq

class TopNFieldStatistic(TrafficStatistic):
    def __init__(self, n = 1, statistic_delay = 10):
        self.n = n
        self.statistic_delay = statistic_delay

    def calculate_statistic(self, recent_loglines: List[Type[LogLine]]) -> None:
        counts = self._add_counts_for_new_lines(recent_loglines)
        top_n = self.get_top_n_fields(counts)
        self.print_top_n_field(top_n)

    def _add_counts_for_new_lines(self, recent_loglines: List[Type[LogLine]]) -> Dict[Any, int]:
        counts = {}
        for logline in recent_loglines:
            field = self.get_field_from_logline(logline)
            counts[field] = counts.get(field, 0) + 1

        return counts

    def get_top_n_fields(self, counts: Dict[Any, int]) -> List[Tuple[str, int]]:
        H = []
        for field, count in counts.items():
            heapq.heappush(H, (-count, field))

        top_n_fields = []
        for _ in range(min(self.n, len(H))):
            count, field = heapq.heappop(H)
            top_n_fields += [(field, -1 * count)]

        return top_n_fields
    
    @abc.abstractmethod
    def get_field_from_logline(self, logline: Type[LogLine]) -> Any:
        pass

    @abc.abstractmethod   
    def print_top_n_field(self, top_n_fields: List[Tuple[str, int]]):
        pass
