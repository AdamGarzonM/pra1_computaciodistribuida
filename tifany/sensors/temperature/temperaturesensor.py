#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import random

#hostname
broker="tifany_mqtt"
topic = f"Gateway/{broker}/temperature"

while True:
    message = random.randint(15,30)
    payload = str(message) + "/" + str(time.time()) + "/temperature"

    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal")
    print(f"Sent payload: {payload} // Topic: {topic}")
    
    time.sleep(2)
    