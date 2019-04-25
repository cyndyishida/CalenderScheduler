import datetime as dt
from collections import namedtuple
from typing import List

Event = namedtuple('Event', 'day, start_time, end_time')
FinalTime = namedtuple('FinalTime', 'day, start_time, end_time, busy_count')
Weights = namedtuple('Weights', 'people, time')

ZERO_TIME = dt.timedelta(hours=0, minutes=0, seconds=0)
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
    0  : Weights(.9 , .1), # care more about people vs time
    1  : Weights(.5 , .5)
}

class SortedNode:
    def __init__(self, data, pri):
        self._data = data
        self._numbusy = 0
        self._full_time = ZERO_TIME
        self._score = self._compute_score(pri)
        self._duration = self._data[0].duration * len(self._data)


    def _compute_score(self,pri):
        # lower score is better?
        curr_duration= ZERO_TIME
        num_busy = 0
        for sch in self._data:
            if not sch.open:
                curr_duration = ZERO_TIME
                num_busy = max(sch.raw_count, num_busy)
            else:
                curr_duration += sch.duration
            if curr_duration > self._full_time:
                self._full_time = curr_duration

        if self._full_time == ZERO_TIME:
            # here we found 0 desired times so everyone is some degree of busy
            self._numbusy = num_busy
            self._full_time = sch.duration * len(self._data)
        else:
            # we found a shorter time slot that everyone is free
            self._numbusy = 0
        time_weight = (self._full_time /sch.duration ) * PRIORITIES[pri].time
        people_weight = -(self._numbusy * PRIORITIES[pri].people ) + 1
        return time_weight + people_weight

    def event_cast(self):
        result = FinalTime(self._data[0]._day, self._data[0]._start, 
                self._data[0]._start + self._full_time, self._numbusy)
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
        if self._size == self._capacity and node > self._data[-1]:
            return # don't bother adding elements that is greater (worse score) 
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


"""
FUNCTIONS
"""
def get_date_from_str(obj) :
    '''
    obj must be in format yyy-mm-dd
    '''
    yr, mth, day = obj.split('-')
    return  dt.date(year=int(yr), month=int(mth), day=int(day))

def get_time_from_str(obj):
    '''
    obj must be in format hh:mm:ss
    '''
    hr, mint, sec = [int(i) for i in obj.split(':')]
    timeobj =dt.time(hr,mint,sec)
    return dt.datetime.combine(dt.date.min, timeobj) - dt.datetime.min

def get_time_from_dt(obj):
    obj = obj.time()
    return dt.datetime.combine(date.min, obj) - datetime.min


def parse_best_time_string(time):
    best_time = time.split()[1:5]
    best_time.pop(2)
    date, start, end = best_time 
    s_hr = start[:start.index(':')]
    e_hr = end[:end.index(':')]
    start = f"{0 if len(s_hr) == 1 else ''}{start}:00"
    end = f"{0 if len(e_hr) == 1 else ''}{end}:00"
    # date conversion
    date = date.split('/')
    date = f"{date[-1]}-{date[0]}-{date[1]}"
    start = f"{date}T{start}-04:00"
    end = f"{date}T{end}-04:00"
    return start, end 

