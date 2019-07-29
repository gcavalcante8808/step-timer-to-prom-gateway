#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import os

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from step_timer import retrieve_time_step_object_from_pickled_file, TimedStep


PROMETHEUS_GATEWAY = os.getenv('PROMETHEUS_GATEWAY_ADDR', 'http://localhost:9091')


def get_step_timed_step(resource=None):
    if not resource:
        retrieve_time_step_object_from_pickled_file(resource=resource)

    return retrieve_time_step_object_from_pickled_file(resource)


def send_timed_step_to_prometheus_gateway(timed_step, job_name):
    # type: (TimedStep, str) -> None
    registry = CollectorRegistry()
    elapsed_time_metric = Gauge('step_elapsed_time_seconds', 'Elapsed time until a step has been finished',
                                ['step_name'], registry=registry)
    elapsed_time_metric.labels(timed_step.step_name).set(timed_step.elapsed_time_in_seconds)

    push_to_gateway(PROMETHEUS_GATEWAY, job=job_name, registry=registry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--resource', type=str, required=True)
    parser.add_argument('--job', type=str, required=False, default='Default')
    args = parser.parse_args()

    timed_step = get_step_timed_step(args.resource)

    send_timed_step_to_prometheus_gateway(timed_step=timed_step, job_name=args.job)
