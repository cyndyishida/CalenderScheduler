import core_types as core
import datetime as dt
from typing import List
#import calender_read as msft
#import google_cal_quickstart as ggl

def parse_txt(input_file) -> List[core.Event]:
    d_len = 10 # expected date input YYYY-MM-DD
    t_len = 8 # expected time input HH:MM:00
   
    user_events = [] 
    input_file.readline() # skip headr 
    for line in input_file:
        year, month, day = line[0:d_len].split('-')
        u_date = dt.date(int(year),int(month), int(day))
        hour, minute, sec = line[d_len+1:d_len+t_len+1].split(':')
        st_time = dt.timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec))
        # iffy??
        e_sep = d_len+1+t_len+1
        end_time = dt.timedelta(minutes=int(line[e_sep:e_sep+2]))
        end_time += st_time

        user_events.append(core.Event(u_date, st_time, end_time))
    return user_events 


def parse_from_google():
    return ggl.get_events(dt.datetime.now(), dt.datetime.now() + dt.timedelta(days=7))

def parse_from_outlook():
    return msft.get_events(dt.datetime.now(), dt.datetime.now() + dt.timedelta(days=7))


if __name__ == '__main__':
    pass 
