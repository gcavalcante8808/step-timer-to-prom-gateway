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
    ./step_timer.py --moment end
```

## Summary

After executing `start` and `end` moment you can view the result stored by passing `summary` to moment:

```bash
    ./step_timer.py --moment summary 
```

## Send to Prometheus Gateway

If you just executed the steps above an file named `current_job.timer` hold a `TimedStep` object persisted with pickle.
You can send it to a prometheus gateway using the following commands:

```bash
    export PROMETHEUS_GATEWAY_ADDR=http://localhost:9091
    ./send_to_prometheus_gateway --resource 'current_step.timer'
```
