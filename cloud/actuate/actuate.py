from kafka import KafkaConsumer
import time
import paho.mqtt.publish as publish
from json import loads
from time import sleep

raw_topic = 'raw'  # Utilitza el mateix tema al qual es subscriu l'altre microservei
broker = "albert_mqtt"
temp_topic = f"Actuate/{broker}/temperature"
presence_topic = f"Actuate/{broker}/presence"

while True:
    try:
        actuate_consumer = KafkaConsumer(
            raw_topic,
            bootstrap_servers = ['kafka : 9092'],
            group_id = 'actuate_service',
            auto_offset_reset = 'latest',
            enable_auto_commit = True,
            value_deserializer = lambda x: loads(x.decode('utf-8'))
        )
        
        if __name__ == "__main__":
            print("ACTUATE")
            for message in actuate_consumer:
                #value='32/1700928523.6854231/presence/dakota_mqtt
                actuate_message = message.value.split("/")
                msg_topic = actuate_message[2]
                msg_value = actuate_message[0]
                if (msg_topic == "temperature" and msg_value >= 18 and msg_value <= 20):
                    mqtt_message = 20
                    payload = str(message) + "/" + time.time()
                    publish.single(topic = temp_topic+"/albert", payload = payload, hostname = "host.docker.internal")

                if (msg_topic == "temperature" and msg_value >= 24 and msg_value <= 28):
                    mqtt_message = 24
                    payload = str(message) + "/" + time.time()
                    publish.single(topic = temp_topic+"/albert", payload = payload, hostname = "host.docker.internal")

                #Presence pot anar sol perquè per tots valors, enviarà un missatge. Temperature no, perquè hi ha certs valors on no s'envia re
                if (msg_topic == "presence"):
                    if(msg_value >= 50):
                        mqtt_message = 1
                    else:
                        mqtt_message = 0
                    payload = str(message) + "/" + time.time()
                    publish.single(topic = presence_topic, payload = payload, hostname = "host.docker.internal")

    except: #NoBrokersAvailable
        sleep(1)
        pass