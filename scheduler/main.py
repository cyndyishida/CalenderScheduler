import schedule as sh


def main():
    # build representation of graph of possible elements interests outside of user events 
    grid = sh.build_grid()

    team_events = [] # call all users  
    try: 
        team_events =sh.ps.parse_from_google() + sh.ps.parse_from_outlook() 
        sh.load_user_schedule(grid, team_events)
        #sh.pprint(grid)
        events = sh.generate_best_time_with_buffer(grid)
        values = sh.pprint_best_times(events, limit = 5)
        print()
        print()
        print(values)
        print()
        print()
    except: 
        print("Unable to find optimial time, try again later.")
    

if __name__ == '__main__':
    main()
