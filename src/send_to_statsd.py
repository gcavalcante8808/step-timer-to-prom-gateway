# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys

import statsd

sys.path.insert(0, '../')

from src.shared import get_timed_step

STATSD_HOST = os.getenv('STATSD_HOST', None)


class StatsDGateway(object):
    def __init__(self, host, port=8125, prefix=''):
        self.host = host
        self.port = port
        self.prefix = prefix

        self.client = statsd.StatsClient(self.host, self.port, self.prefix)

    def send_gauge(self, metric, value):
        self.client.gauge(metric, value)

    def send_timer(self, metric, value):
        raise NotImplementedError

    def send_incr(self, metric, value):
        raise NotImplementedError


def send_timed_step_elapsed_time_in_seconds_to_statsd(resource,
                                                      gateway,
                                                      statsd_metric_name
                                                      ):
    # type: (str, StatsDGateway, str) -> (str, int)
    timed_step = get_timed_step(resource)
    gateway.send_gauge(statsd_metric_name, timed_step.elapsed_time_in_seconds)

    return statsd_metric_name, timed_step.elapsed_time_in_seconds


def get_cli_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--resource', type=str, required=True)
    parser.add_argument('--host', type=str, required=False, default=STATSD_HOST)
    parser.add_argument('--port', type=int, required=False, default=8125)
    parser.add_argument('--metric', type=str,required=True)
    parser.add_argument('--prefix', type=str, required=False, default='default')

    return parser


def parse_cli_args(parser):
    args = parser.parse_args()
    if not args.host:
        raise Exception("You must provide an value for --host or set STATSD_HOST to the statsd host address.")

    return args


if __name__ == '__main__':
    cli_parser = get_cli_parser()

    args = parse_cli_args(cli_parser)

    gateway = StatsDGateway(host=args.host, port=args.port, prefix=args.prefix)
    send_timed_step_elapsed_time_in_seconds_to_statsd(args.resource, gateway, args.metric)
