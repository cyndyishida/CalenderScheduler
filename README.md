# Calender Scheduler

### Algorithm 
*word vomit so I dont forgot what I made* 

Basically I have a 2-D adjacency matrix that represents the master calendar 
where the row represent +5 minute incrementsand the column represents the date. 
Each node has a count of the number of busy people at the time frame. I parse out the calendar text and generate user event nodes. 
Iterate those events and load it into the master grid. After, I do a depth first traversal to find a contiguous (nodes with count 0) space 
that is equivalent to the amount of desired time, to determine the best meeting time.
