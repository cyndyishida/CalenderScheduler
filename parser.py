from core_types import (
    List,
    Event,
    timedelta,
    date,
    time,
    datetime
)

def parse_txt(input_file) -> List[Event]:
    d_len = 10 # expected date input YYYY-MM-DD
    t_len = 8 # expected time input HH:MM:00
   
    user_events = [] 
    input_file.readline() # skip headr 
    for line in input_file:
        year, month, day = line[0:d_len].split('-')
        u_date = date(int(year),int(month), int(day))
        hour, minute, sec = line[d_len+1:d_len+t_len+1].split(':')
        st_time = timedelta(hours=int(hour), minutes=int(minute), seconds=int(sec)) 
        # iffy??
        e_sep = d_len+1+t_len+1
        end_time = timedelta(minutes=int(line[e_sep:e_sep+2]))
        end_time += st_time

        user_events.append(Event(u_date, st_time, end_time))
    return user_events 



if __name__ == '__main__':
    parse_txt(open("/Users/cyndyishida/Projects/Capstone/groupcollabo/dev/scheduler/examples/ggl_example_output.txt")) 
