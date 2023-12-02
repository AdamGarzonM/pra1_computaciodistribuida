from kafka import KafkaConsumer
import paho.mqtt.publish as publish
from json import loads
from time import sleep

topic = 'clean'

def prepareConsumer():
    try:
        actuate_consumer = KafkaConsumer(
            topic,
            bootstrap_servers = ['kafka : 9092'],
            group_id = 'actuate_service',
            auto_offset_reset = 'latest',
            enable_auto_commit = True,
            value_deserializer = lambda x: loads(x.decode('utf-8'))
        )
        return actuate_consumer
    except:
        sleep(1)
        prepareConsumer()

if __name__ == "__main__":
    print("Starting cloud microservice ACTUATE")
    while True:
        try:
            actuate_consumer = prepareConsumer()
            break
        except TypeError as e:
            print(f"Error: {e}; because kafka is not ready, trying again...")
            sleep(2)
    
    for message in actuate_consumer:
        msg_value, _, msg_topic, msg_broker = message.value.split("/")
        msg_value = int(msg_value)
        print(f"ACTUATE is processing message {message}")
        actuator_topic = f"Actuate/{msg_broker}/{msg_topic}"
        if msg_topic == "temperature":
            if msg_value >= 18 and msg_value <= 20:
                payload = 20
                publish.single(actuator_topic, payload, hostname = "host.docker.internal")
                print(f"ACTUATE sent payload {payload} into topic {actuator_topic}")
                continue
            if msg_value >= 24 and msg_value <= 28:
                payload = 24
                publish.single(actuator_topic, payload, hostname = "host.docker.internal")
                print(f"ACTUATE sent payload {payload} into topic {actuator_topic}")
                continue
        if msg_topic == "presence":
            if(msg_value >= 50):
                payload = 1
                publish.single(actuator_topic, payload, hostname = "host.docker.internal")
                print(f"ACTUATE sent payload {payload} into topic {actuator_topic}")
                continue
            else:
                payload = 0
                publish.single(actuator_topic, payload, hostname = "host.docker.internal")
                print(f"ACTUATE sent payload {payload} into topic {actuator_topic}")
                continue
        #Aquest else es per lightbulb i heatpump
        else:
            continue