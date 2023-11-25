from kafka import KafkaConsumer, KafkaProducer
#from kafka import NoBrokersAvailable
from json import loads, dumps
from time import sleep
import os
       

#### FALLA. POSSIBLEMENT PER GRUPS PERÒ NO TENIM CERTESA
kafka_topic = 'raw' 

def prepareKafka():
    try:
        clean_consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers = ['kafka : 9092'],
            group_id = 'clean_service',
            auto_offset_reset = 'latest',
            enable_auto_commit = True,
            value_deserializer = lambda x: loads(x.decode('utf-8'))
        )

        clean_producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda x: dumps(x).encode('utf-8'),
            api_version=(0,11,5), # no se si es necessari
            max_in_flight_requests_per_connection = 1,
        )
        return clean_consumer, clean_producer
    except:
        sleep(1)
        prepareKafka()

if __name__ == "__main__":
    print("CLEAN")
    clean_consumer, clean_producer = prepareKafka()
    for message in clean_consumer: #aqui es llança una excepcio (maybe)
        #value=51/1700950233.1468713/presence/tommy_mqtt'
        value, _, topic, _ = message.value.split("/")
        value = int(value)
        if topic == "temperature" and value >= -18 and value <= 28:
            print(f"CLEAN will try to send {message.value}")
            clean_producer.send("clean", value=message.value)
            print(f"CLEAN has sent {message.value}")
        elif topic == "presence" and value >= 0 and value <= 100:
            print(f"CLEAN will try to send {message.value}")
            clean_producer.send("clean", value=message.value)
            print(f"CLEAN has sent {message.value}")
        else:
            print(f"CLEAN has discarded {message.value}")