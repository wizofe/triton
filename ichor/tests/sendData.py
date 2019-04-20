#
#   Binds REP socket to tcp://*:5555
#	Sends random data

import time
import zmq
import numpy as np
from random import randint

context = zmq.Context()

#  Socket to talk to server
print("Connecting to live data server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s ..." % request)
    #randomNumber = randint(0,9)
    randomNumber = request
    numAsString = str(randomNumber)
    socket.send_string(numAsString)

    #get reply
    message = socket.recv_string()
    print("Received reply %s [ %s ]" % (request, message))