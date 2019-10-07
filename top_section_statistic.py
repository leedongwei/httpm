from traffic_statistic import TrafficStatistic
from logline import LogLine
from typing import Type, Dict, List
import operator

class TopSectionStatistic(TrafficStatistic):
    def __init__(self, statistic_delay = 10):
        self.statistic_delay = statistic_delay

    def calculate_statistic(self, recent_loglines: List[Type[LogLine]]) -> None:
        section_counts = self._add_section_counts_for_new_lines(recent_loglines)
        top_section, hits = self._get_top_section(section_counts)
        self._print_top_section(top_section, hits)

    def _add_section_counts_for_new_lines(self, recent_loglines) -> Dict[str, int]:
        section_counts = {}
        for logline in recent_loglines:
            section = logline.get_section()
            section_counts[section] = section_counts.get(section, 0) + 1

        return section_counts

    def _get_top_section(self, section_counts) -> str:
        top_section = max(section_counts.items(), key=operator.itemgetter(1))[0] if section_counts.items() else None
        if top_section:
            return top_section, section_counts[top_section]
        return None, None
        
    def _print_top_section(self, top_section: str, hits: int):
        print('The section with the most hits in the last {} seconds is: {}'.format(self.statistic_delay, top_section))
        print('Hits: {}'.format(hits))
