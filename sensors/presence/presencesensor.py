#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time, random, os

#broker="albert_mqtt"
broker = os.environ.get("BROKER")
topic = f"Gateway/{broker}/presence" 

while True:
    message = random.randint(-10,110)
    payload = str(message) + "/" + str(time.time()) + "/presence"
    port = int(os.environ.get("PORT"))
    print(port)
    publish.single(topic = topic, payload = payload, hostname = "host.docker.internal", port=port)
    print(f"Sent payload: {payload} // Topic: {topic}")
    
    time.sleep(5)
    