import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from os import environ
from time import time

pump = 20
port = int(environ.get("PORT"))
broker = environ.get("BROKER")


def on_message(client, userdata, msg):
    global pump
    data = msg.payload.decode()
    print(f"Heatpump received payload: {data} from {broker}")
    newpump = int(data.split('/')[0])
    if pump != newpump:
        pump = newpump  
        payload = str(pump) + "/" + str(time()) + "/heatpump"
        print(f"Pump is now: {pump}")
        ttopic = f"Gateway/{broker}/temperature"
        publish.single(topic = ttopic, payload = payload, hostname = "host.docker.internal", port=port)
        print(f"Sent payload: {payload} Topic: {ttopic}")

if __name__ == "__main__":
    topic = f"Actuate/{broker}/temperature"
    print(f"HEATPUMP with {broker} subscribing to {topic}...")
    subscribe.callback(on_message, topic, hostname="host.docker.internal")
    