#
#   Binds REP socket to tcp://*:5555
#   Expects data from sendData.py, appends and plots
#

import time
import zmq
import matplotlib.pyplot as plt
import numpy as np
import pylab as p

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

#prepare empty array
array = []
x_array = []

# set up plot
plt.ion()
plt.show()
plt.plot(x_array, array)
plt.axis([0, 10, 0, 10])
plt.draw()
plt.pause(0.001)

while True:
    #  Wait for next request from client
    message = socket.recv_string()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(0.5)

    #Convert data back to int
    data = [int(message)]

    #Append new data
    array.extend(data)

    #match length
    x_array = np.linspace(0, len(array) - 1, len(array))

    plt.plot(x_array, array)
    plt.draw()
    plt.pause(0.001)

    plt.autoscale(True)

    socket.send_string("Data received and plotted")
