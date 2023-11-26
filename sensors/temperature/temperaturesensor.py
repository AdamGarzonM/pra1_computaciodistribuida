import paho.mqtt.publish as publish
from time import sleep, time
from random import randint
from os import environ

broker = environ.get("BROKER")
topic = f"Gateway/{broker}/temperature"
port = int(environ.get("PORT"))

while True:
    message = randint(15,30)
    payload = str(message) + "/" + str(time()) + "/temperature"
    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal", port = port)
    print(f"Sent payload: {payload} Topic: {topic}")
    
    sleep(2)
    