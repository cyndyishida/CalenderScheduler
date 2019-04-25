from scheduler.schedule import * 
import datetime as dt
import scheduler.core_types as core

if __name__ == '__main__':


    calender = MeetingCalendar()
    user_events = []
    user_events.append(core.Event(AUTO_PREF_START_DATE,
                             dt.timedelta(hours=8, minutes=11),
                             dt.timedelta(hours=19, minutes=55) ))
    user_events.append(core.Event(AUTO_PREF_START_DATE,
                                dt.timedelta(hours=8, minutes=11),
                                dt.timedelta(hours=15, minutes=20) ))
    user_events.append(core.Event(AUTO_PREF_START_DATE + dt.timedelta(days=1),
                                dt.timedelta(hours=8, minutes=11),
                                dt.timedelta(hours=15, minutes=20) ))
    calender.load_user_schedule(user_events)
    print(calender)
    events = calender.generate_best_times()
    result = beautify(events)
    print(result)
    print(serialize_events(events))

