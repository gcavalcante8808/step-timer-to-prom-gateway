import datetime

from slugify import slugify

from src.step_timer import manage_step_timer, retrieve_time_step_object_from_pickled_file, TimedStep


class TestTimedStep(object):

    def test_persists_timed_step_object_correctly_when_moment_is_start(self):
        resource_name = 'shu.timer'

        step_timer = manage_step_timer(step_name='SHU STEP', moment='start', resource=resource_name)
        persisted_step_timer = retrieve_time_step_object_from_pickled_file(resource=resource_name)

        assert persisted_step_timer
        assert step_timer.start_time == persisted_step_timer.start_time
        assert step_timer.step_name == persisted_step_timer.step_name
        assert persisted_step_timer.step_name == slugify('SHU STEP')

    def test_persists_timed_step_object_correctly_when_moment_is_end(self):
        resource_name = 'shu.timer'

        manage_step_timer(step_name='SHU STEP', moment='start', resource=resource_name)
        step_timer = manage_step_timer(step_name='SHU STEP', moment='end', resource=resource_name)
        persisted_step_timer = retrieve_time_step_object_from_pickled_file(resource=resource_name)

        assert persisted_step_timer
        assert step_timer.start_time == persisted_step_timer.start_time
        assert step_timer.step_name == persisted_step_timer.step_name
        assert step_timer.end_time == persisted_step_timer.end_time
        assert type(step_timer.end_time - step_timer.end_time) == datetime.timedelta

    def test_return_elapsed_time_in_seconds_when_passed_through_all_moments(self):
        fifteen_minutes_in_seconds = datetime.timedelta(minutes=15).total_seconds()
        step_timer = TimedStep(step_name='SHU')

        step_timer.start_time = datetime.datetime(year=2019, month=7, day=12, hour=9, minute=30)
        step_timer.end_time = datetime.datetime(year=2019, month=7, day=12, hour=9, minute=45)

        assert fifteen_minutes_in_seconds == step_timer.elapsed_time_in_seconds
