# Task Manager CLI

This is my CLI task manager application utilizing a **microservice architecture**

## Getting Started

1. Initialize you virtual env

```cmd
python3 -m venv env
source env/bin/activate
```

2. Install specified packages

```cmd
pip install -r requirements.txt
```

## Sevice A

Service A is an API client that recieves a string of coordinates and uses them to fetch a 16 day forecast for the given location.

### Request data

Example client side via ZeroMQ

```py
import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(1):
    print(f"Sending request {request} …")
    coordinates = {"lat": "44.34", "lon": "10.9"}

    # stringify the coordinates
    coords_str = str(coordinates)
    socket.send_string(coords_str)

    #  Get the reply.
    message = socket.recv_json()
    deserialized_message = json.loads(message)
    print(f"Received json reply: {deserialized_message}")

```

### Recieve data

The below is an example server code block to accept and process data from the client

```py
while True:
    #  Wait for next request from client
    message = socket.recv()
    # print(f"Received request: {message}")
    decoded_message = message.decode(encoding="utf-8")
    # convert str to dict
    dic = ast.literal_eval(decoded_message)

    """ Some execution logic"""

    #  Send reply back to client
    socket.send_json(json.dumps(body))

```

## Resources

To learn more about JSON communication via ZeroMQ referer to the template directory
