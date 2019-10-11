# httpm - Datadog interview take-home assignment

## How to run

1. Setup virtual environment

```
python3 -m venv venv
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run `httpm`

```
python3 httpm.py [<OPTIONS>] PATH_TO_LOG
```

With extra configuration:

```
python3 httpm.py test.log -th 2 -adi 30 --traffic-stats response_codes request
_size
```

Run `httpm` with the `--help` flag to see which options are configurable (such as the high traffic threshold, statistics delay, and alert delay).

## Log simulation script

To test the log monitor, I wrote a script to simulate a live http access log using the `sample_csv.txt` file which was provided to me. 

To run the simulation:
1. Run the log simulation script

```
python3 logger.py
```

2. In another shell, run `httpm`

```
python3 httpm.py test.log
```

## Design

There are five main classes in my design.

### LogConsumer

`LogConsumer` is responsible for reading in lines from the target log file and writing them to the `LogKeep`.

### LogKeep

`LogKeep` is a container for the log lines. It only holds log lines that have been read within the last
`alert_delay_interval` seconds.

### Alerter

`Alerter` is responsible for determining if any alert was triggered based on the log lines from the last `alert_delay_interval` seconds.

### TrafficStatistic

The `TrafficStatistic` classes are responsible for calculating different statistics based on the log lines from the last `stats_delay_interval` seconds. Adding a new statistic is easy: just implement the `TrafficStatistic` interface.

### Monitor

`Monitor` represents the system as a whole. It uses the classes described above to implement the functionality of an http access log monitor. 

## Program flow

1. `LogConsumer` reads new lines from the log file and adds them to `LogKeep`. 
2. Every `stats_delay_interval` seconds, `Monitor` reads the loglines from the last `stats_delay_interval` seconds to calculate statistics and output them. 
3. Every `alert_delay_interval` seconds, `Monitor` outputs an alert if one was triggered within the last `alert_delay_interval` seconds.

**NOTE**:

`Monitor` continuously checks if an alert was triggered, but only outputs an alert to the console at every interval. The time posted in the alert is **the time at which the alert was triggered**, not the current time (when the alert is output to the console).

### Tests

Test are written with `unittest`. To run:

```
python3 -m unittest tests.py
```

### Possible improvements

- Better organization of files into submodules (folders...)

- One possible improvement could be to use filesystem events to notify the monitor when new lines are written to the log file, instead of continuously polling it. 

- In terms of scalability, I would be interested in possibly expanding on the `LogKeep` idea, but using something like    `RabbitMQ ` instead. I am not sure, however, if this is overkill for a simple log monitor program. 

- Have more statistics.

- Have different alerts (e.g. several requests originating from the same ip? Lots of `500` response codes?, etc.)

- Notifications for alerts (email, sms?)

- Actions on alert (e.g. make a request to some other server in response to certain alerts)

- Nice console banner, colors, or even a gui
