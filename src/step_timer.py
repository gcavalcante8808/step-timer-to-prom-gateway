#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import pickle
from datetime import datetime

from slugify import slugify


class TimedStep(object):
    def __init__(self, step_name, start_time=None, end_time=None):
        self.step_name = step_name
        self.start_time = start_time
        self.end_time = end_time

    @property
    def elapsed_time_in_seconds(self):
        elapsed_time = self.end_time - self.start_time
        return elapsed_time.total_seconds()


def write_time_step_file(obj, resource):
    # type: (TimedStep, str) -> None
    with open(resource, 'wb') as timefile:
        pickle.dump(obj, timefile)


def retrieve_time_step_object_from_pickled_file(resource):
    # type: (str) -> TimedStep
    with open(resource, 'rb') as timefile:
        return pickle.load(timefile)


def manage_step_timer(step_name, moment, resource='current_step.timer'):
    if 'start' in moment:
        step_timer = TimedStep(step_name=slugify(step_name), start_time=datetime.now())
        write_time_step_file(step_timer, resource=resource)
        return step_timer

    if 'end' in moment:
        step_timer = retrieve_time_step_object_from_pickled_file(resource=resource)
        step_timer.end_time = datetime.now()
        write_time_step_file(step_timer, resource=resource)
        return step_timer

    if 'summary' in moment:
        step_timer = retrieve_time_step_object_from_pickled_file(resource=resource)
        print("Ran {} in {} seconds".format(step_timer.step_name, step_timer.elapsed_time_in_seconds))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage Step Times.')
    parser.add_argument('--moment', choices=['start', 'end', 'summary'], required=True)
    parser.add_argument('--step_name', required=True)
    parser.add_argument('--resource', type=str, required=False, default='current_step.timer')
    args = parser.parse_args()

    timed_step = manage_step_timer(args.step_name, args.moment, args.resource)
