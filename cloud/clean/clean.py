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
    clean_consumer, clean_producer = prepareKafka() #aixo funcionava als altres aqui no idk (maybe)
    for message in clean_consumer: #aqui es llança una excepcio (maybe)
        #value='25/1700859867.9161658/temperature'
        tmessage = message.value.split("/")
        topic = tmessage[2]
        value = int(tmessage[0])
        if topic == "temperature" and value >= -18 and value <= 28:
            print("s'entra a l'if")
            clean_producer.send("clean", value=message.value)
                    