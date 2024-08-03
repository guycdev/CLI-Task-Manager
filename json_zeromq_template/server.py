#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")
    decoded_message = message.decode(encoding="utf-8")
    dic = {"Hello": decoded_message}
    body = json.dumps(dic)
    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send_json(body)
