import time

from typing import Type, List
from log_consumer import LogConsumer
from logkeep import LogKeep
from alerter import Alerter
from traffic_statistic import TrafficStatistic

class HTTPLogMonitor:
    def __init__(
        self, 
        consumer: Type[LogConsumer],
        logkeep: Type[LogKeep],
        alerter: Type[Alerter],
        traffic_stats: List[Type[TrafficStatistic]],
        stats_delay_interval: int = 10,
    ):
        self.consumer = consumer
        self.logkeep = logkeep
        self.alerter = alerter
        self.stats_delay_interval = stats_delay_interval
        self.traffic_stats = traffic_stats

    def run(self):
        next_stats_time = time.time() + self.stats_delay_interval
        next_alert_time = time.time() + self.alerter.alert_check_interval

        last_alert = None
        while True:
            # Consume the next lines from the log
            self.consumer.consume_next_lines()

            # We continuously check for an alert so that we can know the exact time it occured
            self._check_if_alert()

            # we only print at every <alert_delay> interval
            current_time = time.time()
            if current_time >= next_alert_time:
                alert = self.alerter.get_alert()
                if alert and alert is not last_alert:
                    print(alert)
                    last_alert = alert
                else:
                    print('No new alerts generated in the last {} seconds. Most recent alert: {}'.format(self.alerter.alert_check_interval, last_alert))
                print()
                next_alert_time = current_time + self.alerter.alert_check_interval

            if current_time >= next_stats_time:
                self._calculate_stats()
                next_stats_time = current_time + self.stats_delay_interval
        
        # Buffer before we poll again
        time.sleep(0.250)

    def _calculate_stats(self):
        recent_loglines = self.logkeep.read_recent_loglines(from_last_n_seconds=self.stats_delay_interval)
        for statistic in self.traffic_stats:
            statistic.calculate_statistic(recent_loglines)
        print('-----------------------------')

    def _check_if_alert(self):
        recent_loglines = self.logkeep.read_recent_loglines(from_last_n_seconds=self.alerter.alert_check_interval)
        self.alerter.check_if_alert(recent_loglines)

    def _clear_alert(self):
        self.alerter.last_alert = None

