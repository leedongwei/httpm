import argparse
import threading
import time

from log_consumer import LogConsumer
from logkeep import LogKeep
from alerter import Alerter
from monitor import HTTPLogMonitor
from top_n_sections import TopNSectionsStatistic
from top_n_response_codes import TopNResponseStatusCodes
from average_request_size_statistic import AverageRequestSizeStatistic

parser = argparse.ArgumentParser(description='A simple HTTP access log monitor')
parser.add_argument('FILE_PATH', type=str, help='path to the access log file to monitor')
parser.add_argument('-th', '--traffic-threshold', type=int, nargs=1, dest='HIGH_TRAFFIC_THRESHOLD', help='requests/s threshold above which high traffic alerts will be generated', default=10)
parser.add_argument('-sdi', '--stats-delay-interval', type=int, nargs=1, dest='STATS_DELAY_INTERVAL', help='interval at which the monitor will calculate stats, in seconds', default=10)
parser.add_argument('-adi', '--alert-delay-interval', type=int, nargs=1, dest='ALERT_DELAY_INTERVAL', help='interval at which the monitor will check for alerts, in seconds', default=120)
parser.add_argument('-st', '--traffic-stats', nargs='?', dest='TRAFFIC_STATS', choices=['response_codes','request_size'], help='additional traffic stats to measure', default=[])
parser.add_argument('-tn', '--top-n', type=int, dest='TOP_N_VALUE', help='the "N" value to be used by "Top N" statistics', default=3)

args = parser.parse_args()
FILE_PATH = args.FILE_PATH
HIGH_TRAFFIC_THRESHOLD = args.HIGH_TRAFFIC_THRESHOLD
STATS_DELAY_INTERVAL = args.STATS_DELAY_INTERVAL
ALERT_DELAY_INTERVAL = args.ALERT_DELAY_INTERVAL 
TRAFFIC_STATS = args.TRAFFIC_STATS
TOP_N_VALUE = args.TOP_N_VALUE

def create_traffic_statistics(requested_stats, top_n_value=3):
    default_stats = [TopNSectionsStatistic(n=top_n_value, statistic_delay=STATS_DELAY_INTERVAL)]
    if 'response_codes' in requested_stats:
        default_stats += [TopNResponseStatusCodes(n=top_n_value, statistic_delay=STATS_DELAY_INTERVAL)]
    if 'request_size' in requested_stats:
        default_stats += [AverageRequestSizeStatistic(n=top_n_value, statistic_delay=STATS_DELAY_INTERVAL)]
    
    return default_stats

def main():
    print('Monitoring {}...'.format(FILE_PATH))
    next_stats_time = time.time() + STATS_DELAY_INTERVAL
    next_alert_time = time.time() + ALERT_DELAY_INTERVAL
    while True:
        # Consume the next lines from the log
        consumer.consume_next_lines()

        # We continuously check for an alert so that we can know the exact time
        # at which an alert was triggered, but we only print at every two-minute interval
        if monitor.has_alert() and time.time() >= next_alert_time:
            alert = monitor.get_alert()
            print(alert)
            next_alert_time = time.time() + ALERT_DELAY_INTERVAL

        #
        if time.time() >= next_stats_time:
            monitor.calculate_stats()
            next_stats_time = time.time() + STATS_DELAY_INTERVAL
        
        # Buffer before we poll again
        time.sleep(0.250)

logkeep = LogKeep()
consumer = LogConsumer(FILE_PATH, logkeep)
alerter = Alerter(ALERT_DELAY_INTERVAL, HIGH_TRAFFIC_THRESHOLD)
traffic_stats = create_traffic_statistics(TRAFFIC_STATS)
monitor = HTTPLogMonitor(logkeep, alerter, traffic_stats, stats_delay_interval=STATS_DELAY_INTERVAL)

main()
