# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from src.step_timer import retrieve_time_step_object_from_pickled_file, TimedStep


def get_timed_step(resource):
    # type: (str) -> TimedStep
    return retrieve_time_step_object_from_pickled_file(resource)
