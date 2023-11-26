import paho.mqtt.subscribe as subscribe
from os import environ

lightbulb = 0

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    lightbulb = int(data.split('/')[0])

    print(f"Lightbulb received payload: {data} from {broker}")
    print(f"Lightbulb is now: {lightbulb}")

if __name__ == "__main__":
    #broker = "albert_mqtt"
    broker = environ.get("BROKER")
    topic = f"Actuate/{broker}/presence"
    print(f"LIGHTBULB with {broker} subscribing to {topic}...")
    subscribe.callback(on_message, topic, hostname="host.docker.internal")
    