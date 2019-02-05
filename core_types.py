from collections import namedtuple
from datetime import (
    timedelta,
    date,
    time,
    datetime
)
from typing import List 

Time = namedtuple('Time', 'day, start_time, end_time')
Event = namedtuple('Event', 'day, start_time, end_time')

class ScheduleNode:
    __slots__ = '_day', '_start', '_end', '_taken_count'

    def __init__(self, day: date = date(1970, 1, 1), start: timedelta =timedelta(), 
                    end: timedelta =timedelta()) -> None :
        self._day = day 
        self._start = start 
        self._end = end
        self._taken_count = 0 

    def is_open(self) -> bool:
        return self._taken_count == 0 

    def in_time_slot(self, day: date, end: timedelta) -> bool: 
        # only actually care about the users time 
        in_time = day == self._day and end >= self._end
        if in_time: 
            self._taken_count += 1 
        return in_time 

    def get_rtime(self) -> timedelta:
        return self._start

    def get_rday(self) -> date:
        return self._day

    def get_time(self) -> str:
        return str(self._start)

    def get_date(self) -> str:
        return str(self._day)

    def get_count(self) -> str:
        return f'{self._taken_count}'

    def __repr__(self) -> str:
        return f'{self._day}: {self._start}-{self._end}\n'

    __str__ = __repr__

