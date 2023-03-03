import random
import math
Q_LIMIT = 100
BUSY = 1
IDLE = 0
def expon(mean):
     #return an exponential random variate with mean "mean"
     return -1.0*mean*math.log(random.random())
#initializing state variables

#initializing the simulation clock

sim_time = 0

#initialize the state variables
server_status = IDLE
num_in_q = 0
time_last_event = 0

#initialize the statistical counters
num_custs_delayed = 0
total_of_delays = 0.0
area_num_in_q = 0
area_server_status = 0.0

#initialize event list. Since no customers are present, the departure(service completion) event is eliminated from consideration

infile = open("mm1.in", "r")
outfile = open("mm1.out", "w")

mean_interarrival = float(infile.readline())
mean_service = float(infile.readline())
num_delays_required = float(infile.readline())

time_next_event = [0.0]*3
time_arrival = [0]*(Q_LIMIT+1)

time_next_event[1] = sim_time + expon(mean_interarrival)
time_next_event[2] = 10**30

def timing(_num_events):
    global sim_time

    min_time_next_event = 1 * 10**29
    next_event_type = 0

    #determine the event type of the next event to occur

    for i in range(1, _num_events+1):
        print(f"Evenet {i}")
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
    
    #check to see whether the event list is empty
    if next_event_type == 0:
        # the event list is empty, so stop the simulation
        outfile.write(f"\nEvent list empty at time {sim_time}")
        #remember to exit the whole program
    
    #the event list is not empty, so advance teh simulation clock
    sim_time = min_time_next_event
    return next_event_type

def arrive(_mean_interarrival, _mean_service):
    global server_status
    global num_in_q
    global total_of_delays
    global num_custs_delayed
    #define the delay variable here
    #schedule next arrival

    time_next_event[1] = sim_time + expon(_mean_interarrival)

    #heck to see whether the server is busy

    if server_status == BUSY:
        #server is busy, so increment number of customers in queue
        num_in_q+=1

        #check to see whether an overflow condition exists

        if num_in_q > Q_LIMIT:
            #the queue has overflowed, so stop the simulation
            outfile.write(f"\nOverflow of the array time_arrival at time {sim_time}")
        
        #there is still room in the queue, so store the time of arrrival of the arriving customer at the (new) end of time_arrival
        time_arrival[num_in_q] = sim_time
    else:
        #server is idle, so arriving customer has delay of zero.
        delay = 0
        total_of_delays += delay

        #increment the number of customers delayed, and make server busy
        num_custs_delayed +=1
        server_status = BUSY
        
        #SCHEDULE A DEPARTURE (service completion)
        time_next_event[2] = sim_time + expon(_mean_service)

def depart(_mean_service):
    global num_in_q
    global total_of_delays
    global num_custs_delayed
    global server_status
    #initialize the delay

    #check to see whether the queue is empty

    if num_in_q == 0:
        #the queue is empty so make the server idle and eliminate the departure (service completion) even from consideration
        server_status = IDLE
        time_next_event[2] = 1*10**30
    else:
        #the queue is nonempty, so decerement teh number of customers in queue
        num_in_q -= 1

        #compute the delay of the customer who is beginning service and the total delay accumulator
        delay = sim_time - time_arrival[1]
        print(delay)
        total_of_delays +=delay

        #increment the number of custoomers delayed, and schedule deparrture
        num_custs_delayed +=1
        time_next_event[2] = sim_time + expon(_mean_service)

        #move each customer in queue (if any) up one place
        for i in range(1, num_in_q+1):
            time_arrival[i] = time_arrival[i+1]

def report():
    #compute and write estimates of desired measures of performance
    print(total_of_delays)
    print(num_custs_delayed)
    print(area_num_in_q)
    print(sim_time)
    print(area_server_status)
    outfile.write(f"\n\nAverage delay in queue minutes {total_of_delays/num_custs_delayed} minutes\n\n ")
    outfile.write(f"Average number in queue {area_num_in_q / sim_time}\n\n")
    outfile.write(f"Server utilization {area_server_status / sim_time}\n\n")
    outfile.write(f"Time simulation ended {sim_time} minutes")

def update_time_avg_stats():
    global time_last_event
    global area_num_in_q
    global area_server_status
    global server_status
    #compute time sice last event , and update last-event-time marker
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    #update are under number-in-queue function
    area_num_in_q += (num_in_q*time_since_last_event)
    area_server_status += (server_status * time_since_last_event)
    print(f"Area_S {area_server_status}")
    print(f"S_s {server_status}")
    print(f"t_S {time_since_last_event}")

def main():
    global num_custs_delayed
    global num_delays_required
    #specify the number of events for teh timing function
    num_events = 2

    #read input parameters
    
    #write report heading and input parameters
    outfile.write("Single-server queueing system\n\n")
    outfile.write(f"Mean interarrival time {mean_interarrival} minutes\n\n")
    outfile.write(f"Mean service time {mean_service} minutes\n\n")
    outfile.write(f"Number of customers {num_delays_required} \n\n")

    #run teh simulation while more delays are still needed
    while (num_custs_delayed < num_delays_required):
        #determine the next event
        next_event_type = timing(num_events)
        print(next_event_type)

        #update time-average statistical accumulators
        update_time_avg_stats()

        #invoke the appropriate event function
        match next_event_type:
            case 1:
                arrive(mean_interarrival, mean_service)
                break
            case 2:
                depart(mean_service)
                break
        
        #invoke the report generator and end the simulation
    report()
    infile.close()
    outfile.close()

main()
