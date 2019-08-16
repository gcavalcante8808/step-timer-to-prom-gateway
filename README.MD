## Command Timer

[![Build Status](https://cloud.drone.io/api/badges/gcavalcante8808/step-timer-to-prom-gateway/status.svg)](https://cloud.drone.io/gcavalcante8808/step-timer-to-prom-gateway)

![Coverage Report](https://codecov.io/gh/gcavalcante8808/step-timer-to-prom-gateway/branch/master/graph/badge.svg)

## How to Use

Before the action that you want to time, run the following statement:

```bash
    ./step_timer.py --moment start --step_name "Name of Step"
```

Run any command normally and then write the end moment with the following command:

```bash
    ./step_timer.py --moment end --step-name "Name of Step"
```

## Summary

After executing `start` and `end` moment you can view the result stored by passing `summary` to moment:

```bash
    ./step_timer.py --moment summary --step-name "Name of Step"
```

**If you just executed the steps above an file named `current_job.timer` hold a `TimedStep` object persisted with pickle.**

Supported args:
 * moment: Start, End or Summary
 * step_name: The name of the step that will be timed.
 * resource: The name of resource file that will be created (`current_step.timer` by default)

## Send to StatsD (or StatsD Exporter)

You can send it to a statsd host using the following commands:
```bash
   export STATSD_HOST=localhost
   ./send_to_statsd --resource 'current_step.timer' --metric "my.own.metric"
```

## Send to Prometheus Gateway

You can send it to a prometheus gateway using the following commands:

```bash
    export PROMETHEUS_GATEWAY_ADDR=http://localhost:9091
    ./send_to_prometheus_gateway.py --resource 'current_step.timer'
```

Supported args:
 * resource: Resource created by the `step_timer.py`;
 * job: Name of the job that will be used on prometheus_gateway (`Default` by default :D)
 * prometheus_gateway_addr: URL address of the prometheus gateway (if not passed the env var `PROMETHEUS_GATEWAY_ADDR` will be used instead).
 
 ### Binary Releases
 
 You can find some binary releases created with `pyinstaller` that can be used by any linux with glibc support (`alpine` is not supported yet because it needs a muslibc build)