import numpy as np
import matplotlib.pyplot as plt

print("Starting")

array = []
x_array = []

# set up plot
plt.ion()
plt.show()
plt.plot(x_array, array)
plt.axis([0, 10, 0, 10])
plt.draw()
plt.pause(0.001)

for meow in range(10):
    print("Using %s " % meow)

    array.extend([meow])
    x_array = np.linspace(0, len(array) - 1, len(array))

    plt.plot(x_array, array)
    plt.draw()
    plt.pause(0.001)
