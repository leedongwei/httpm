import time

def log():
    with open('./sample_csv.txt', 'r') as inf:
        with open('test.log', 'w', buffering=1) as testl:
            while True:
                line = inf.readline()
                if line:
                    print(line)
                    testl.write(line)
                time.sleep(1)

log()