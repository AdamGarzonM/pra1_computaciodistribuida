import paho.mqtt.subscribe as subscribe
import os

pump = 20

def on_message(client, userdata, msg):
    data = msg.payload.decode() + "/" + broker
    pump = data.split('/')[0]

    print(f"Heatpump received payload: {data}.")
    print(f"Pump is now: {pump}")

if __name__ == "__main__":
    #broker = "albert_mqtt"
    broker = os.environ.get("BROKER")
    subscribe.callback(on_message, f"Actuate/{broker}/temperature/albert", hostname="host.docker.internal")
    