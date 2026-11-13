import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Queue settings
arrival_rate = 1.0
service_rate = 1.5
num_customers = 40

# Generate exponential random time
def exp_time(rate):
    return random.expovariate(rate)




# Customer arrival times 
#arrival_times = [0.5, 0.8, 2.0, 2.8, ...]  # 40 customers total

arrival_times = []
current_time = 0

for _ in range(num_customers):
    current_time += exp_time(arrival_rate)
    arrival_times.append(current_time)


# Customer service times
# service_times = [0.4, 0.7, 0.3, 0.9, ...]  # 40 customers total
service_times = []

for _ in range(num_customers):
    service_times.append(exp_time(service_rate))

# Store service start and finish times 
#start_times = [0.5, 0.9, 2.0, 2.8, ...]
#finish_times = [0.9, 1.6, 2.3, 3.7, ...]


start_times = []
finish_times = []

for i in range(num_customers):

    # First customer starts immediately
    if i == 0:
        start = arrival_times[i]

    # Others wait if server is busy
    else:
        start = max(arrival_times[i], finish_times[i - 1])

    # Service finish time
    finish = start + service_times[i]

    start_times.append(start)
    finish_times.append(finish)

# Data for graph
time_points = []
queue_lengths = []

current_time = 0
ultimate_end_time = finish_times[-1]

# Calculate customers in system over time
while current_time <= ultimate_end_time:

    current_queue = 0
    i = 0

    # Count arrived customers
    while i < num_customers and arrival_times[i] <= current_time:
        current_queue += 1
        i += 1

    j = 0

    # Remove served customers
    while j < num_customers and finish_times[j] <= current_time:
        current_queue -= 1
        j += 1

    # Save graph points
    time_points.append(current_time)
    queue_lengths.append(current_queue)

    current_time += 0.1

# Create graph
fig, ax = plt.subplots()

ax.set_title("Single Server Queue Simulation")
ax.set_xlabel("Time")
ax.set_ylabel("Customers in System")

line, = ax.plot([], [], lw=2)

ax.set_xticks(range(0, int(time_points[-1]) + 1, 1))

ax.set_xlim(0, time_points[-1])
ax.set_ylim(0, max(queue_lengths) + 1)

# Update animation frame
def update(frame):

    line.set_data(time_points[:frame], queue_lengths[:frame])

    return line,

# Animate graph
ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(time_points),
    interval=50,
    blit=True
)

# Show graph
plt.show()