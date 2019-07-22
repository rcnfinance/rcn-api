from functools import total_ordering
from models import ClockModel
from db import connection


@total_ordering
class Clock():
    def __init__(self):
        self._clock = self._get_or_create()

    def _get_or_create(self):
        clock = ClockModel.objects.get_clock()
        if not clock:
            clock = self._create()
        return clock

    def _create(self):
        clock = ClockModel()
        clock.time = str(0)
        clock.save()
        return clock

    def _save(self):
        self._clock.save()

    def advance_to(self, value):
        if value > self.time:
            self._clock.time = str(value)
            self._save()

    def reset(self):
        self._clock.time = '0'
        self._save()

    @property
    def time(self):
        return int(self._clock.time)

    def __repr__(self):
        return "Clock({})".format(self.time)

    def __str__(self):
        return "The clock's time is {}".format(self.time)

    def __eq__(self, other_time):
        return self.time == other_time

    def __lt__(self, other_time):
        return self.time < other_time

    def __add__(self, other_time):
        return self.time + other_time

    def __radd__(self, other_time):
        return self.time + other_time

    def __sub__(self, other_time):
        return self.time - other_time

    def __rsub__(self, other_time):
        return self.time - other_time
