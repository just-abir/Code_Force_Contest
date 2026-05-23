import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


arrival_rate = 1.0      # jei rate e customer ra ashbe
service_rate = 1.5      # jei rate e server oderke service dite parbe
simulation_time = 40    # ✅ simulate 40 minutes (time units)


def exp_time(rate):
    return random.expovariate(rate)

# This function generates a single sample from an exponential distribution
# with parameter 'rate' (λ).


# ✅ Generate arrival times UNTIL simulation_time is reached
customer_id=1
arrival_times = []
current_time = 0
while current_time < simulation_time:
    current_time += exp_time(arrival_rate)
    if current_time < simulation_time:  # ✅ Only add if within 40 minutes
        arrival_times.append(current_time)
        print(f"[ARRIVAL] Customer-{customer_id} arrived at time {current_time:.2f}")
        customer_id += 1


# ✅ Generate service times for each customer who actually arrived
service_times = []
for i in range(len(arrival_times)):
    service = exp_time(service_rate)
    service_times.append(service)
    print(f"[SERVICE TIME] Customer-{i+1} service time = {service:.2f}")

# Calculate start and finish times for each customer
start_times = []
finish_times = []

for i in range(len(arrival_times)):
    if i == 0:
        start = arrival_times[i]
    else:
        start = max(arrival_times[i], finish_times[i-1])
    
    finish = start + service_times[i]
    
    start_times.append(start)
    finish_times.append(finish)
    
    # ✅ Print statements HERE
    print(f"\nCustomer-{i+1}")
    print(f"Arrival Time : {arrival_times[i]:.2f}")
    print(f"Start Time   : {start:.2f}")
    print(f"Finish Time  : {finish:.2f}")
    print(f"Waiting Time : {start - arrival_times[i]:.2f}")


# Track queue length over time
time_points = []
queue_lengths = []

current_time = 0
# ultimate_end_time = max(simulation_time, finish_times[-1]) if finish_times else simulation_time  # ✅ Go until min 40 or until last customer finishes

ultimate_end_time = simulation_time  # ✅ Go until 40 minutes only

while current_time <= ultimate_end_time:
    current_queue = 0
    
    # Count how many have ARRIVED by current_time
    i = 0
    while i < len(arrival_times) and arrival_times[i] <= current_time:  # ✅
        current_queue += 1
        i += 1
    
    # Subtract how many have FINISHED by current_time
    j = 0
    while j < len(finish_times) and finish_times[j] <= current_time:  # ✅
        current_queue -= 1
        j += 1
    
    time_points.append(current_time)
    queue_lengths.append(current_queue)
    print(f"[QUEUE] Time={current_time:.1f} -> Queue Length={current_queue}")
    current_time += 0.1


# Calculate average queue length
average_queue_length = sum(queue_lengths) / len(queue_lengths) if queue_lengths else 0
print(f"\n Average Queue Length per Unit Time: {average_queue_length:.2f} customers")

# Calculate average waiting time
waiting_times = []
for i in range(len(arrival_times)):
    waiting_time = start_times[i] - arrival_times[i]
    waiting_times.append(waiting_time)

average_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
print(f"  Average Waiting Time: {average_waiting_time:.2f} time units")
print(f" Total Customers: {len(arrival_times)}")
print(f" Average Service Time: {sum(service_times) / len(service_times):.2f} time units\n")


# Create and display animated graph
fig, ax = plt.subplots()

ax.set_title("Single Server Queue Simulation (40 Minutes)")
ax.set_xlabel("Time")
ax.set_ylabel("Number of Customers in System")

line, = ax.plot([], [], lw=2)

ax.set_xticks(range(0, int(time_points[-1]) + 1, 5))
ax.set_xlim(0, time_points[-1])
ax.set_ylim(0, max(queue_lengths) + 1)

def update(frame):
    line.set_data(time_points[:frame], queue_lengths[:frame])
    return line,

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(time_points),
    interval=50,
    blit=True
)

plt.show()