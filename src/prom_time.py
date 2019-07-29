# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import pickle
from datetime import datetime
from tempfile import TemporaryFile
from uuid import uuid4

import click
from slugify import slugify


class TimedStep(object):
    def __init__(self, step_name, start_time=None, end_time=None):
        self.identifier = uuid4()
        self.step_name = step_name
        self.start_time = start_time
        self.end_time = end_time

    @property
    def elapsed_time_in_seconds(self):
        elapsed_time = self.end_time - self.start_time
        return elapsed_time.total_seconds()


def write_time_step_file(obj, resource='current_job.timer'):
    # type: (TimedStep, str) -> None
    with open(resource, 'wb') as timefile:
        pickle.dump(obj, timefile)


def retrieve_time_step_object_from_pickled_file(identifier, resource='current_job.timer'):
    # type: (uuid4, str) -> TimedStep
    with open(resource, 'rb') as timefile:
        return pickle.load(timefile)


def manage_step_timer(identifier, step_name, moment, resource=None):
    if 'start' in moment:
        step_timer = TimedStep(step_name=slugify(step_name), start_time=datetime.now())
        write_time_step_file(step_timer)
        print("START - StepTimer created for step: {} with uuid {}".format(step_timer.step_name, step_timer.identifier))
        return step_timer

    if 'end' in moment:
        step_timer = retrieve_time_step_object_from_pickled_file(identifier=identifier)
        step_timer.end_time = datetime.now()
        write_time_step_file(step_timer)
        print("END - StepTimer updated for step: {} with uuid {}".format(step_timer.step_name, step_timer.identifier))
        return step_timer
