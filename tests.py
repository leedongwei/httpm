from logline import LogLine
import sys
import unittest
import logging

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class LogLineTest(unittest.TestCase):
    def test_from_line(self):
        line = "\"10.0.0.2\",\"-\",\"apache\",1549573860,\"GET /api/user HTTP/1.0\",200,1234"
        log_line = LogLine.from_line(line)
        self.assertEqual(log_line.bytes, 1234)

    def test_get_section(self):
        log_line = LogLine(request='/api/user')
        section = log_line.get_section()
        self.assertEqual(section, '/api')