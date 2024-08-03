import zmq
import json
import requests
import os
from dotenv import load_dotenv
import ast


load_dotenv()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

key = os.environ.get("KEY")


def fetch_weather_data(coordinates: dict):
    req = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={coordinates['lat']}&lon={coordinates['lon']}&cnt=16&appid={key}"
    )
    resp = req.json()
    print(resp)
    return json.dumps(resp)


while True:
    #  Wait for next request from client
    message = socket.recv()
    # print(f"Received request: {message}")
    decoded_message = message.decode(encoding="utf-8")
    dic = ast.literal_eval(decoded_message)
    body = fetch_weather_data(dic)
    #  Send reply back to client
    socket.send_json(json.dumps(body))
