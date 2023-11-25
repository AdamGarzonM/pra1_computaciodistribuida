import paho.mqtt.subscribe as subscribe
import os

lightbulb = 0

def on_message(client, userdata, msg):
    data = msg.payload.decode() + "/" + broker
    lightbulb = data.split('/')[0]

    print(f"Lightbulb received payload: {data}.")
    print(f"Lightbulb is now: {lightbulb}")

if __name__ == "__main__":
    #broker = "albert_mqtt"
    broker = os.environ.get("BROKER")
    subscribe.callback(on_message, f"Actuate/{broker}/presence/albert", hostname="host.docker.internal")
    