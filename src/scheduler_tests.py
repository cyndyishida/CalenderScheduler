import schedule as sh
import datetime as dt
import core_types as core

def test_build_grid_default():
    cal = sh.MeetingCalendar()
    grid = cal._grid
    assert grid[0][0]._day == sh.AUTO_PREF_START_DATE
    assert grid[0][0]._start == dt.timedelta(minutes=sh.AUTO_PREF_START_TIME)
    assert grid[-1][-1]._day ==  sh.AUTO_PREF_START_DATE + dt.timedelta(days=sh.DAY_SPAN-1)
    assert len(grid) == sh.DAY_SPAN
    assert len(grid[0]) == (sh.AUTO_PREF_END_TIME - sh.AUTO_PREF_START_TIME) // sh.GRANULARITY 

def test_build_grid_params():
    start = 14 * 60 # 2 pm 
    end = 16 * 60 # 4 pm 
    gran = 10 # ten minute increments 
    cal = sh.MeetingCalendar(step = gran, start_time=start,end_time=end, span=1) # find next day
    grid = cal._grid
    assert grid[0][0]._day == sh.AUTO_PREF_START_DATE
    assert grid[0][0]._start == dt.timedelta(minutes=start)
    assert grid[-1][-1]._day == sh.AUTO_PREF_START_DATE
    assert len(grid) == 1
    assert len(grid[0]) == (end - start) // gran 

def test_load_user_schedule():
    # set up 
    date = dt.date(year=2019, month=1, day=20)
    span = 1  
    start = 14 * 60 # 2 pm 
    end = 16 * 60 # 4 pm 
    step = 10 
    cal = sh.MeetingCalendar(step=step, start_date = date, start_time=start, end_time=end, span=span)
    events = [sh.core.Event(date, dt.timedelta(minutes=start), dt.timedelta(minutes=start+15))]
    cal.load_user_schedule(events)
    for i in range( 15 // step ):
        assert not cal._grid[0][i].open

def test_generate_best_time_with_buffer_best():
    # set up 
    date = dt.date(year=2019, month=1, day=20)
    span = 1  
    start = 14 * 60 # 2 pm 
    end = 16 * 60 # 4 pm 
    cal = sh.MeetingCalendar(start_date = date, start_time=start, end_time=end, span=span)
    events = [sh.core.Event(date, dt.timedelta(minutes=start), dt.timedelta(minutes=start+15))]
    cal.load_user_schedule(events)
     
