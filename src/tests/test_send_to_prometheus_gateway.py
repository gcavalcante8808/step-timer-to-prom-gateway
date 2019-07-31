#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import six
from slugify import slugify

from src.send_to_prometheus_gateway import set_elapsed_time_in_seconds_metric_value_and_send_to_prometheus_gateway, get_timed_step, \
    PrometheusGateway, create_collector_registry, create_elapsed_time_in_seconds_gauge_metric
from src.step_timer import manage_step_timer

if six.PY3:
    from unittest.mock import patch
else:
    from mock import patch


class TestSendToPrometheusGateway(object):
    def setup_class(self):
        self.metric_name = 'step_elapsed_time_seconds'
        self.metric_description = 'Elapsed time until a step has been finished'
        self.labels = 'step_name'
        self.registry = create_collector_registry()
        self.gateway = gateway = PrometheusGateway(registry=self.registry, prometheus_gateway_addr='')
        self.metric = create_elapsed_time_in_seconds_gauge_metric(self.metric_name,
                                                                  self.metric_description,
                                                                  [self.labels],
                                                                  gateway.registry)
        self.job_name = 'TestJob'

    def test_can_send_a_timed_step_object_to_prometheus_gateway(self):
        resource_name = 'prom.timer'
        step_name = 'PROM STEP'
        manage_step_timer(step_name='PROM STEP', moment='start', resource=resource_name)
        manage_step_timer(step_name='PROM STEP', moment='end', resource=resource_name)
        timed_step = get_timed_step(resource=resource_name)

        with patch.object(PrometheusGateway, 'send', return_value=None) as mocked_prometheus_gateway_send:
            set_elapsed_time_in_seconds_metric_value_and_send_to_prometheus_gateway(resource=resource_name,
                                                                                    job_name='TestJob',
                                                                                    gateway=self.gateway,
                                                                                    metric=self.metric)
        sample_data = self._get_prometheus_metric_sample(self.metric_name, self.labels, step_name)

        assert sample_data
        assert type(sample_data) == float
        assert sample_data == timed_step.elapsed_time_in_seconds
        assert mocked_prometheus_gateway_send.called

    def _get_prometheus_metric_sample(self, metric_name, label, label_value):
        return self.registry.get_sample_value(metric_name, {label: slugify(label_value)})
