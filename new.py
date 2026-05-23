import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


arrival_rate = 1.0   # Customer arrival rate (per unit time)
service_rate = 1.5   # Server service rate (per unit time)
num_customers = 40   # Total number of customers in the simulation


# Exponential random time generate korar function
# Queueing theory te arrival ar service duita usually exponential distribution follow kore
def exp_time(rate):
    return random.expovariate(rate)



# =========================
# CUSTOMER ARRIVAL TIMES
# =========================

arrival_times = []   # Sob customer kokhon arrive korbe ta store korar list
current_time = 0

# Prottek customer-er arrival time generate kora hocche
# Inter-arrival time exponential distribution theke ashbe
for _ in range(num_customers):

    # Previous arrival time er sathe new random gap add kortesi
    current_time += exp_time(arrival_rate)

    # Final arrival time list e save kortesi
    arrival_times.append(current_time)



# =========================
# SERVICE TIMES
# =========================

service_times = []   # Prottek customer-er service duration store korar list

# Random service time generate kortesi
for _ in range(num_customers):

    # Exponential distribution theke service time generate
    service_times.append(exp_time(service_rate))



# =========================
# SERVICE START & FINISH TIMES
# =========================

start_times = []    # Customer kokhon service start korbe
finish_times = []   # Customer kokhon service finish korbe

# Ekek customer-er service start ar finish time calculate kortesi
for i in range(num_customers):

    # First customer directly arrival er sathe service pabe
    if i == 0:
        start = arrival_times[i]

    else:
        # Service start hobe:
        # 1. Customer arrival er por
        # 2. Previous customer finish korar por
        # Ei duitar moddhe jeta later, oitai actual start time
        start = max(arrival_times[i], finish_times[i - 1])

    # Finish time = Start time + Service duration
    finish = start + service_times[i]

    # Calculated values store kortesi
    start_times.append(start)
    finish_times.append(finish)



# =========================
# QUEUE LENGTH CALCULATION
# =========================

# Graph bananor jonno time ar queue/system size store korbo
time_points = []

# NOTE:
# Ekhane "queue_lengths" name use korleo,
# actually amra puro system e kotojon ase oita count kortesi:
# (Waiting queue + currently served customer)
queue_lengths = []

current_time = 0

# Simulation cholbe last customer finish kora porjonto
ultimate_end_time = finish_times[-1]


while current_time <= ultimate_end_time:

    # Current time e system e koyjon ase
    current_queue = 0

    i = 0

    # Ei porjonto jara arrive korse tader count kortesi
    while i < num_customers and arrival_times[i] <= current_time:
        current_queue += 1
        i += 1

    j = 0

    # Ei porjonto jara service finish kore chole gese tader bad ditesi
    while j < num_customers and finish_times[j] <= current_time:
        current_queue -= 1
        j += 1

    # Current state graph er jonno save kortesi
    time_points.append(current_time)
    queue_lengths.append(current_queue)

    # Time step increase
    # Prottek 0.1 unit time por system observe kortesi
    current_time += 0.1



# =========================
# GRAPH & ANIMATION
# =========================

fig, ax = plt.subplots()

ax.set_title("Single Server Queue Simulation")

ax.set_xlabel("Time")

# System e total customer count
# = waiting + currently being served
ax.set_ylabel("Number of Customers in System")


# Empty line initialize
line, = ax.plot([], [], lw=2)

# X-axis ticks set
ax.set_xticks(range(0, int(time_points[-1]) + 1, 1))

# Axis limits
ax.set_xlim(0, time_points[-1])
ax.set_ylim(0, max(queue_lengths) + 1)



# Animation update function
# Prottek frame e graph aste aste draw hobe
def update(frame):

    line.set_data(
        time_points[:frame],
        queue_lengths[:frame]
    )

    return line,


# Animation object create
ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(time_points),
    interval=50,
    blit=True
)

# Final graph show
plt.show()