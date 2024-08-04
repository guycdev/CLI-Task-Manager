#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(1):
    print(f"Sending request {request} …")
    coordinates = {"lat": "44.34", "lon": "10.9"}
    coords_str = str(coordinates)
    socket.send_string(coords_str)

    #  Get the reply.
    message = socket.recv_json()

    # Decode json
    decoded_message = json.loads(message)
    print(f"Received json reply {decoded_message}")
