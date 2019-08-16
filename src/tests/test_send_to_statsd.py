#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import six


from src.send_to_statsd import send_timed_step_elapsed_time_in_seconds_to_statsd
from src.step_timer import manage_step_timer, retrieve_time_step_object_from_pickled_file, TimedStep

if six.PY3:
    from unittest.mock import Mock
else:
    from mock import Mock


class TestSendToStatsd(object):
    def setup_class(self):
        self.metric_name = 'step_elapsed_time_seconds'
        self.metric_description = 'Elapsed time until a step has been finished'
        self.labels = 'step_name'

    def test_can_send_a_timed_step_object_to_statsd_server(self):
        resource_name = 'statsd.timer'
        manage_step_timer(step_name='PROM STEP', moment='start', resource=resource_name)
        manage_step_timer(step_name='PROM STEP', moment='end', resource=resource_name)
        timed_step = retrieve_time_step_object_from_pickled_file(resource=resource_name)
        author = 'gcavalcante8808'
        metric_type = 'unittests'
        statsd_metric_name = '{}.{}.{}.{}'.format(self.metric_name, author, metric_type, timed_step.step_name)


        metric_name, metric_value = send_timed_step_elapsed_time_in_seconds_to_statsd(
            resource=resource_name,
            gateway=Mock(),
            statsd_metric_name=statsd_metric_name)

        assert metric_name == statsd_metric_name
        assert metric_value == timed_step.elapsed_time_in_seconds
