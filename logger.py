import time
import random

def get_random_sleep_value():
    return random.random() + random.random()

def log():
    with open('./sample_csv.txt', 'r') as inf:
        with open('test.log', 'w', buffering=1) as testl:
            while True:
                line = inf.readline()
                if line:
                    print(line)
                    testl.write(line)
                time.sleep(get_random_sleep_value())

log()