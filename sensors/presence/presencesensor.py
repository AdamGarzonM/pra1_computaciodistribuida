#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import random

#hostname
broker="albert_mqtt"
topic = "Gateway/{broker}/presence"

while True:
    message = random.randint(-10,110)
    payload = str(message) + "/" + str(time.time()) + "/presence"

    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal")
    
    time.sleep(5)
    