import paho.mqtt.subscribe as subscribe
import os

pump = 20

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    pump = int(data.split('/')[0])

    print(f"Heatpump received payload: {data} from {broker}")
    print(f"Pump is now: {pump}")

if __name__ == "__main__":
    #broker = "albert_mqtt"
    broker = os.environ.get("BROKER")
    topic = f"Actuate/{broker}/temperature"
    print(f"HEATPUMP with {broker} subscribing to {topic}...")
    subscribe.callback(on_message, topic, hostname="host.docker.internal")
    