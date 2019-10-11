from top_n_statistic import TopNFieldStatistic
from logline import LogLine
from typing import Type, List, Tuple, Any

class TopNResponseStatusCodes(TopNFieldStatistic):
    def __init__(self, n=1, statistic_delay=10):
        super().__init__(n=n, statistic_delay=statistic_delay)
        
    def get_field_from_logline(self, logline: Type[LogLine]) -> Any:
        return logline.status

    def print_top_n_field(self, top_n_fields: List[Tuple[str, int]]):
        print('The top {} response codes over the last {} seconds:'.format(self.n, self.statistic_delay))
        for code, count in top_n_fields:
            print('\tResponse Code: {}, Hits: {}'.format(code, count))
        print()
