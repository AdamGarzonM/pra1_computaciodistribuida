#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import random

#hostname
broker="albert_mqtt"
topic = "Gateway/{broker}/temperature"

while True:
    message = random.randint(15,30)
    payload = str(message) + "/" + str(time.time()) + "/temperature"

    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal")
    #hostname podem fer hostname: cosa
    
    time.sleep(5)
    