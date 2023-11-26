from kafka import KafkaConsumer
import time
import paho.mqtt.publish as publish
from json import loads
from time import sleep

topic = 'clean'  # Utilitza el mateix tema al qual es subscriu l'altre microservei
broker = "albert_mqtt"
temp_topic = f"Actuate/{broker}/temperature"
presence_topic = f"Actuate/{broker}/presence"

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
    actuate_consumer = prepareConsumer()
    for message in actuate_consumer: #aqui es llança una excepcio
        #topic dels actuadors:
        # Actuate/albert_mqtt/temperature/albert.
        #ConsumerRecord(topic='raw', partition=0, offset=146, timestamp=1700942514435, timestamp_type=0, key=None, value='96/1700942514.4258428/presence/tommy_mqtt', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=43, serialized_header_size=-1)
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

        #Presence pot anar sol perquè per tots valors, enviarà un missatge. Temperature no, perquè hi ha certs valors on no s'envia re
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
