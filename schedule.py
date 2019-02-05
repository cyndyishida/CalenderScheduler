from core_types import (
    List,
    ScheduleNode,
    Time,
    Event,
    timedelta,
    date,
    time,
    datetime
)
from parser import parse_txt
from typing import Optional

DAY_SPAN = 7 
AUTO_PREF_START_TIME = 17 * 60 
AUTO_PREF_END_TIME  = 19 * 60
AUTO_PREF_START_DATE = date.today() + timedelta(days=1)
GRANULARITY = 5
DESIRED_TIME_AMOUNT = 60

'''
helper functions 
'''
def round_minutes(day: date, time: timedelta, resolution: int) -> timedelta:
    result = datetime(day.year, day.month, day.day) + time 
    new_minute = (result.minute // resolution) * resolution
    result += timedelta(minutes=new_minute - result.minute)
    return timedelta(hours = result.hour, minutes = result.minute, seconds = result.second)


def get_idx(start: timedelta, curr: timedelta, increment: int) -> int:
    # figure out distance of current time to the indexed value on grid 
    return int(((curr.total_seconds() - start.total_seconds()) // 60 ) / increment)


def generate_best_time_helper(grid: [List[ScheduleNode]], allotted: int = 60, row: int = 0, col: int = 0) -> Optional[ScheduleNode]:
    if row >= len(grid) and col >= len(grid[0]):
        return None
    desired_count = allotted / GRANULARITY # allotted is in minutes
    gained_count = 0
    stop = False
    while col< len(grid[0]) and gained_count < desired_count and not stop:
        if grid[row][col].is_open():
            gained_count += 1
        else:
            stop = True
        col += 1

    if col >= len(grid[0]) and desired_count != gained_count:
        row += 1
        col = 0

    return grid[row][col-gained_count] if desired_count == gained_count \
            else generate_best_time_helper(grid, allotted, row, col)

'''
Master functions 
'''

def load_user_schedule(master_grid: List[List[ScheduleNode]], 
                        user_events: List[Event]) -> None:
    initial = master_grid[0][0].get_rtime()
    max_steps = len(master_grid[0])
    for event in user_events:
        day, start, end = event 
        days_diff = (event.day - AUTO_PREF_START_DATE).days
        if days_diff >= 0 and days_diff < DAY_SPAN:
            start_boundary = round_minutes(day, start, GRANULARITY)
            start_idx = get_idx(initial, start_boundary, GRANULARITY)
            end_boundary = round_minutes(day, end, GRANULARITY)
            end_idx = get_idx(initial, end_boundary, GRANULARITY)
            start_idx = 0 if start_idx < 0 else start_idx 
            end_idx = max_steps if end_idx > max_steps else end_idx 
            for i in range(start_idx, end_idx):
                if not master_grid[days_diff][i].in_time_slot(day, end):
                    raise Exception('Misstep in calculation')


def build_grid(step: int, start: int, 
                end: int, day: date) -> List[List[ScheduleNode]]:
    return [[ScheduleNode(AUTO_PREF_START_DATE + timedelta(days=i) ,
                timedelta(minutes=j), timedelta(minutes=j+step)) for j in range(start, end, step)]
                    for i in range(DAY_SPAN)]


def generate_best_time(grid: [List[ScheduleNode]], allotted: int = 60) -> Optional[Event]:
    # allotted should represent amount of minutes desired
    event = generate_best_time_helper(grid, allotted, 0, 0)
    return Event(event.get_rday(), event.get_rtime(), event.get_rtime()+ timedelta(minutes=allotted)) if event else None


def pprint_best_time(event: Optional[Event]) -> None:
    if event:
        print(f'\nBest Determined Time: {event.day} {event.start_time} - {event.end_time}')
    else:
        print("UNABLE TO DETERMINE BEST TIME")


def pprint(grid: List[List[ScheduleNode]]) -> None:
    # generate pretty print grid template 
    dates  = [i[0].get_date() for i in grid]
    allocator = len(dates[0]) + 1 
    dates.insert(0, " " * (allocator-2)) 

    # actually print the contents in grid 
    print("|".join(dates))

    for col in range(len(grid[0])):
        el = grid[0][col].get_time()
        parsed_line = f'{el:{allocator}}'
        for row in range(len(grid)): 
            el = grid[row][col].get_count()
            parsed_line += f"{el:{allocator}}"
            
        print(parsed_line)


if __name__ == '__main__':
    
    grid = build_grid(GRANULARITY, AUTO_PREF_START_TIME, 
                        AUTO_PREF_END_TIME, AUTO_PREF_START_DATE)

    #print("\n".join(str(node) for node in grid))
    #print("Generate Pretty Graph")
    print("After loading users calender data")
    user_events = parse_txt(open("/Users/cyndyishida/Projects/Capstone/groupcollabo/dev/scheduler/examples/ggl_example_output.txt"))
    # example dates 
    user_events.append(Event(date(2019, 2, 6),
                                timedelta(hours=17, minutes=11),
                                timedelta(hours=18, minutes=54) ))
    user_events.append(Event(date(2019, 2, 7), 
                                timedelta(hours=16, minutes=11), 
                                timedelta(hours=18, minutes=50) ))
    user_events.append(Event(date(2019, 2, 7),
                             timedelta(hours=16, minutes=11),
                             timedelta(hours=18, minutes=50) ))
    user_events.append(Event(date(2019, 2, 7),
                             timedelta(hours=18, minutes=11),
                             timedelta(hours=18, minutes=50) ))
    load_user_schedule(grid, user_events)
    load_user_schedule(grid, user_events)
    pprint(grid)

    event = generate_best_time(grid, DESIRED_TIME_AMOUNT)
    pprint_best_time(event)
