import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from os import environ
from time import time

lightbulb = 0
port = int(environ.get("PORT"))
broker = environ.get("BROKER")


def on_message(client, userdata, msg):
    global lightbulb
    data = msg.payload.decode()
    print(f"Lightbulb received payload: {data} from {broker}")
    newlightbulb = int(data.split('/')[0])
    if lightbulb != newlightbulb:
        lightbulb = newlightbulb
        payload = str(lightbulb) + "/" + str(time()) + "/lightbulb"
        print(f"Lightbulb is now: {lightbulb}")
        ttopic = f"Gateway/{broker}/presence"
        publish.single(topic = ttopic, payload = payload, hostname = "host.docker.internal", port=port)
        print(f"Sent payload: {payload} Topic: {ttopic}")

if __name__ == "__main__":
    topic = f"Actuate/{broker}/presence"
    print(f"LIGHTBULB with {broker} subscribing to {topic}...")
    subscribe.callback(on_message, topic, hostname="host.docker.internal")
    