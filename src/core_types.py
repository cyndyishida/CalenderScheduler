import datetime as dt
from collections import namedtuple
from typing import List

Event = namedtuple('Event', 'day, start_time, end_time')
Weights = namedtuple('Weights', 'people, time')
class ScheduleNode:
    __slots__ = '_day', '_start', '_end', '_taken_count', '_step'

    def __init__(self, day: dt.date = dt.date(1970, 1, 1), start: dt.timedelta =dt.timedelta(),
                    end: dt.timedelta = dt.timedelta()) -> None :
        self._day = day 
        self._start = start 
        self._end = end
        self._taken_count = 0
        self._step = end - start

    @property
    def open(self) -> bool:
        return self._taken_count == 0 

    def in_time_slot(self, day: dt.date, end: dt.timedelta, step: dt.timedelta) -> bool:
        # only actually care about the users time
        in_time = day == self._day and (end >= self._end or (self._end  - end) < dt.timedelta(minutes=step))
        if in_time: 
            self._taken_count += 1 
        return in_time

    @property
    def duration(self):
        return self._step

    @property
    def raw_time(self) -> dt.timedelta:
        return self._start

    @property
    def raw_day(self) -> dt.date:
        return self._day

    @property
    def str_time(self) -> str:
        return str(self._start)

    @property
    def str_date(self) -> str:
        return str(self._day)

    @property
    def str_count(self) -> str:
        return f'{self._taken_count}'

    @property
    def raw_count(self):
        return self._taken_count

    def __repr__(self) -> str:
        return f'{self._day}: {self._start}-{self._end}'

    __str__ = __repr__


PRIORITIES = {
    0  : Weights(.7 , .3)
}

class SortedNode:
    def __init__(self, data, pri):
        self._data = data
        self._numbusy = 0
        self._full_time = dt.timedelta(hours=0, minutes=0, seconds=0)
        self._score = self._compute_score(pri)
        self._duration = self._data[0].duration * len(self._data)


    def _compute_score(self,pri):

        curr_duration= dt.timedelta(hours=0, minutes=0, seconds=0)
        for sch in self._data:
            if sch.raw_count  > self._numbusy:
                self._numbusy = sch.raw_count
            if not sch.open:
                curr_duration = dt.timedelta(hours=0, minutes=0, seconds=0)
            else:
                curr_duration += sch.duration
            if curr_duration > self._full_time:
                self._full_time = curr_duration

        time_weight = (self._full_time /sch.duration ) * PRIORITIES[pri].time
        people_weight = -(self._numbusy * PRIORITIES[pri].people ) + 1
        return time_weight + people_weight

    def event_cast(self):
        result = Event(self._data[0]._day, self._data[0]._start, self._data[0]._start + self._full_time)
        return result


    def __gt__(self, other):
        return self._score > other._score

    def __lt__(self, other):
        return self._score < other._score

    def __eq__(self, other):
        return self._score == other._score

    def __repr__(self) -> str:
        return f'{self._data[0].raw_time} = Duration {self._duration} Score {self._score}'

    __str__ = __repr__

class SortedArray:
    def __init__(self, capacity):
        self._data = []
        self._size = 0
        self._capacity = capacity
        self._precedence = self._define_precedence()

    def _define_precedence(self, ordering = None):
        if ordering is None:
            # pick time everyone's all available, then contiguous time
            return 0

    def add(self, el):
        node = SortedNode(el, self._precedence)
        self._size += 1
        if self._size == 1:
            self._data.append(node)
            return
        position = self.search(node)
        self._data.insert(position, node)
        if self._size > self._capacity:
            self.remove()

    def remove(self):
        self._size -=1
        return self._data.pop()

    def search(self, el):
        """
        bisection to determine correct index to add into data
        """
        low = 0
        hi = len(self._data)
        while low < hi:
            mid = (low+hi)//2
            if el > self._data[mid]: hi = mid
            else: low = mid+1
        return low

    def convert_to_events(self):
        return [i.event_cast() for i in self._data]

    def __str__(self):
        return '\n'.join(str(i) for i in self._data)

    __repr__ = __str__
