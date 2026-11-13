import random
import matplotlib.pyplot as plt

inside = 0
total = 50000

x_inside = []
y_inside = []

x_outside = []
y_outside = []

for i in range(total):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)

    if x*x + y*y <= 1:
        inside += 1
        x_inside.append(x)
        y_inside.append(y)
    else:
        x_outside.append(x)
        y_outside.append(y)

print("Total points =", total)
print("Inside circle =", inside)
print("Outside circle =", total-inside)
pi_value = 4 * inside / total

print("Estimated value of pi =", pi_value)

plt.scatter(x_inside, y_inside, color='blue', s=2)
plt.scatter(x_outside, y_outside, color='red', s=2)

plt.title(f"Monte Carlo Simulation of Pi = {pi_value}")
plt.show()