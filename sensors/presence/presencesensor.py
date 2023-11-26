import paho.mqtt.publish as publish
from time import sleep, time
from random import randint
from os import environ

broker = environ.get("BROKER")
topic = f"Gateway/{broker}/presence" 
port = int(environ.get("PORT"))

while True:
    message = randint(-10,110)
    payload = str(message) + "/" + str(time()) + "/presence"
    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal", port=port)
    print(f"Sent payload: {payload} Topic: {topic}")
    
    sleep(5)
    