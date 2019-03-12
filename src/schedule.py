from typing import Optional, List
import datetime as dt
import core_types as core
import parser as ps


DAY_SPAN = 7
# times denote minutes 
AUTO_PREF_START_TIME = 15 * 60
AUTO_PREF_END_TIME  = 17 * 60
AUTO_PREF_START_DATE = dt.date.today() + dt.timedelta(days=1)
GRANULARITY = 15
DESIRED_TIME_AMOUNT = 30
BUFFER_TIME = 0

'''
helper functions 
'''
def round_minutes(day: dt.date, time: dt.timedelta, resolution: int) -> dt.timedelta:
    result = dt.datetime(day.year, day.month, day.day) + time
    new_minute = (result.minute // resolution) * resolution
    result += dt.timedelta(minutes=new_minute - result.minute)
    return dt.timedelta(hours = result.hour, minutes = result.minute, seconds = result.second)

def get_idx(start: dt.timedelta, curr: dt.timedelta, increment: int) -> int:
    # figure out distance of current time to the indexed value on grid 
    return int(((curr.total_seconds() - start.total_seconds()) // 60 ) / increment)


'''
Master functions 
'''
class MeetingCalendar:
    def build_grid(self) -> List[List[core.ScheduleNode]]:
        return [[core.ScheduleNode(self._st_date + dt.timedelta(days=i) ,
                              dt.timedelta(minutes=j), dt.timedelta(minutes=j+self._step))
                 for j in range(self._st_time, self._end_time, self._step)]
                for i in range(self._day_span)]

    def __init__(self, span=DAY_SPAN, start_time=AUTO_PREF_START_TIME, end_time=AUTO_PREF_END_TIME,
                    start_date = AUTO_PREF_START_DATE, step = GRANULARITY):
        self._day_span = span
        self._st_time = start_time
        self._end_time = end_time
        self._st_date = start_date 
        self._step = step
        self._grid = self.build_grid()
        self._best_times = None 

        #num_days = DAY_SPAN 
        #grid = []
        #i = 0
        #while i < num_days:
        #    current_events = []
        #    curr_day = AUTO_PREF_START_DATE + dt.timedelta(days=i)
        #    if curr_day.weekday() not in {5,6}:
        #        for j in range(start, end, step):
        #            current_events.append(core.ScheduleNode(curr_day, dt.timedelta(minutes=j), dt.timedelta(minutes=j+step)))
        #        grid.append(current_events)
        #    else:
        #        num_days += 1 
        #    i += 1 

    def load_user_schedule(self, user_events: List[core.Event]) -> None:
        initial = self._grid[0][0].raw_time
        max_steps = len(self._grid[0])
        for event in user_events:
            day, start, end = event
            days_diff = (event.day - self._st_date).days
            if days_diff >= 0 and days_diff < self._day_span:
                # process correct cells to process into grid
                start_boundary = round_minutes(day, start, self._step)
                end_boundary = round_minutes(day, end, self._step)
                start_idx = get_idx(initial, start_boundary, self._step)
                end_idx = get_idx(initial, end_boundary, self._step)
                start_idx = 0 if start_idx < 0 else start_idx
                end_idx = max_steps-1 if end_idx >= max_steps else end_idx
                # load into grid
                for i in range(start_idx, end_idx + 1 ):
                    sch_node = self._grid[days_diff][i]
    
                    if not sch_node.in_time_slot(day, end, self._step) and  \
                                sch_node.raw_time != end:
                        # boundary check
                        raise Exception('Misstep in calculation')


    def __str__(self) -> None:
        # generate pretty print grid template 
        dates  = [i[0].str_date for i in self._grid]
        allocator = len(dates[0]) + 1 
        dates.insert(0, " " * (allocator-2)) 
    
        # actually print the contents in grid 
        result = ["|".join(dates)]
    
        for col in range(len(self._grid[0])):
            el = self._grid[0][col].str_time
            parsed_line = f'{el:{allocator}}'
            for row in range(len(self._grid)): 
                el = self._grid[row][col].raw_count
                parsed_line += f"{el:^{allocator}}"
                
            result.append(parsed_line)
        return '\n'.join(result)

    __repr__ = __str__


    def generate_best_times(self,  allotted: int = DESIRED_TIME_AMOUNT, buffer = BUFFER_TIME, count = 5) -> Optional[core.Event]:
        # allotted should represent amount of minutes desired
        time_amount = allotted + buffer 
        best_times = core.SortedArray(count)
        desired_count = time_amount // self._step # allotted is in minutes
        events_per_day = len(self._grid[0]) // desired_count
        for d in range(len(self._grid)):
            for t in range(len(self._grid[0])  - events_per_day + 1 ):
                ev = [self._grid[d][i] for i in range(t, t + desired_count)]
                best_times.add(ev)

        self.best_times = best_times.convert_to_events()
        return self.best_times



def beautify(events) -> None:
    result_str = "Possible Optimal Times"
    for event in events:
        day = event.day
        if event.start_time < dt.timedelta(hours=13):
            st = str(event.start_time)[:-3]
            st += " PM" if event.start_time > dt.timedelta(hours=12) else " AM"
        else:
            st = ' ' + str(event.start_time - dt.timedelta(hours=12))[:-3]
            st += " PM"
        if event.end_time < dt.timedelta(hours=13):
            end = str(event.end_time)[:-3]
            end  += " PM" if event.end_time > dt.timedelta(hours=12) else " AM"
        else:
            end = ' '+str(event.end_time - dt.timedelta(hours=12))[:-3]
            end += " PM"
        result_str += f'\n {day:} {st:>{9}}  - {end:>{8}} EST'
    return result_str



if __name__ == '__main__':


    calender = MeetingCalendar()
    user_events = []
    user_events.append(core.Event(dt.date(2019, 3, 12),
                             dt.timedelta(hours=15, minutes=11),
                             dt.timedelta(hours=15, minutes=55) ))
    user_events.append(core.Event(dt.date(2019, 3, 12),
                                dt.timedelta(hours=15, minutes=11),
                                dt.timedelta(hours=15, minutes=20) ))
    calender.load_user_schedule(user_events)
    print(calender)
    events = calender.generate_best_times()
    result = beautify(events)
    print(result)

