#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time, random, os

#broker="albert_mqtt"
broker = os.environ.get("BROKER")
topic = f"Gateway/{broker}/presence" 

while True:
    message = random.randint(-10,110)
    payload = str(message) + "/" + str(time.time()) + "/presence"

    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal")
    print(f"Sent payload: {payload} // Topic: {topic}")
    
    time.sleep(5)
    