#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import os
import sys

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

sys.path.insert(0, '../')

from src.step_timer import retrieve_time_step_object_from_pickled_file, TimedStep

PROMETHEUS_GATEWAY = os.getenv('PROMETHEUS_GATEWAY_ADDR', 'http://localhost:9091')


class PrometheusGateway(object):
    def __init__(self, registry, prometheus_gateway_addr):
        self.registry = registry
        self.prometheus_gateway_addr = prometheus_gateway_addr

    def send(self, job_name):
        # type: (str) -> None
        push_to_gateway(self.prometheus_gateway_addr, job=job_name, registry=self.registry)


def get_timed_step(resource):
    # type: (str) -> TimedStep
    return retrieve_time_step_object_from_pickled_file(resource)


def create_collector_registry():
    registry = CollectorRegistry()
    return registry


def create_elapsed_time_in_seconds_gauge_metric(name,
                                                description,
                                                labels,
                                                registry):
    return Gauge(name, description,
                 labels, registry=registry)


def set_elapsed_time_in_seconds_metric_value(metric, labels, value):
    metric.labels(labels).set(value)


def set_elapsed_time_in_seconds_metric_value_and_send_to_prometheus_gateway(resource, job_name, gateway, metric):
    # type: (str, str, PrometheusGateway, Gauge) -> None
    timed_step = get_timed_step(resource)
    set_elapsed_time_in_seconds_metric_value(metric, timed_step.step_name, timed_step.elapsed_time_in_seconds)
    gateway.send(job_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--resource', type=str, required=True)
    parser.add_argument('--job', type=str, required=False, default='Default')
    parser.add_argument('--prometheus_gateway_addr', required=False, default=PROMETHEUS_GATEWAY)
    args = parser.parse_args()

    gateway = PrometheusGateway(registry=create_collector_registry(),
                                prometheus_gateway_addr=args.prometheus_gateway_addr)

    metric = create_elapsed_time_in_seconds_gauge_metric('step_elapsed_time_seconds',
                                                         'Elapsed time until a step has been finished',
                                                         ['step_name'],
                                                         gateway.registry)

    set_elapsed_time_in_seconds_metric_value_and_send_to_prometheus_gateway(resource=args.resource,
                                                                            job_name=args.job,
                                                                            gateway=gateway,
                                                                            metric=metric)
