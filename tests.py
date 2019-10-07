import os
import sys
import threading
import unittest
from unittest.mock import Mock
import logging
import time

from logline import LogLine
from logkeep import LogKeep
from log_consumer import LogConsumer
from top_section_statistic import TopSectionStatistic

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class LogLineTest(unittest.TestCase):
    def test_from_line(self):
        line = '\"10.0.0.2\",\"-\",\"apache\",1549573860,\"GET /api/user HTTP/1.0\",200,1234'
        log_line = LogLine.from_line(line)
        self.assertEqual(log_line.bytes, 1234)

    def test_get_section(self):
        log_line = LogLine(request='GET /api/user HTTP/1.0')
        section = log_line.get_section()
        self.assertEqual(section, '/api')

class LogKeepTest(unittest.TestCase):
    def test_get_recent_loglines(self):
        logkeep = LogKeep()
        for _ in range(3):
            logkeep.add_logline(LogLine())
            time.sleep(1)

        logger.debug([l.time for l in logkeep.read_recent_loglines()])
        logger.debug([l.time for l in logkeep.read_recent_loglines(2)])

class LogConsumerTest(unittest.TestCase):
    def setUp(self):
        self.logkeep = Mock()
        self.consumer = LogConsumer(self.logkeep)

    def test_write_to_logkeep(self):
        def write_log():
            with open('test.log', 'w') as log:
                logger.debug('Writing to test log...')
                for _ in range(10):
                    log.write('\"10.0.0.2\",\"-\",\"apache\",{},\"GET /api/user HTTP/1.0\",200,1234\n'.format(round(time.time())))
                    time.sleep(0.5)
                logger.debug('Finished writing to log.')
            
            time.sleep(1)
            self.consumer._stop()

        def consume():
            self.consumer.consume_log_file('test.log')
            self.logkeep.add_logline.assert_called()

        t = threading.Thread(target=write_log)
        t.start()
        c = threading.Thread(target=consume)
        c.start()

        t.join()
        c.join()
        os.remove('test.log')
        os.remove('test.log.offset')

class TopSectionStatisticTest(unittest.TestCase):
    def test_calculate_statistic(self):
        statistic = TopSectionStatistic()

        loglines = []
        for _ in range(2):
            line = '\"10.0.0.2\",\"-\",\"apache\",{},\"GET /api/user HTTP/1.0\",200,1234'.format(round(time.time()))
            log_line = LogLine.from_line(line)
            loglines += [log_line]
            time.sleep(1)

        for _ in range(1):
            line = '\"10.0.0.2\",\"-\",\"apache\",{},\"GET /reports HTTP/1.0\",200,1234'.format(round(time.time()))
            log_line = LogLine.from_line(line)
            loglines += [log_line]
            time.sleep(1)

        section_counts = statistic._add_section_counts_for_new_lines(loglines)
        top_section, hits = statistic._get_top_section(section_counts)
        self.assertEqual(top_section, '/api')
        self.assertEqual(hits, 2)