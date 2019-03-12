# Calender Scheduler

### Algorithm 
*word vomit so I dont forgot what I made* 

Basically I have a 2-D adjacency matrix that represents the master calendar 
where the row represent +5 minute incrementsand the column represents the date. 
Each node has a count of the number of busy people at the time frame. I parse out the calendar text and generate user event nodes. 
Iterate those events and load it into the master grid. After, I do a depth first traversal to find a contiguous (nodes with count 0) space 
that is equivalent to the amount of desired time, to determine the best meeting time.

Before this algorithm ran in O(N) time.

Here we have a different optimial goal, 
Generate the X best times, and have a weight that determines what is better than others.
Concept: 
1. generate grid same as always 
2. when determining the best time, add each possible timeslot (allotted time) into my sorted vector3. in th sorted vector, run a bisection algorithm to determine where to add the element by the greater weight. Weight is defined by that time slot, largest continious time slot where everyone can meet, and how many people are busy given that they use up that entire time. 
4. After reading in all possible time slots, return back the X best which are held in the sorted vector object 
