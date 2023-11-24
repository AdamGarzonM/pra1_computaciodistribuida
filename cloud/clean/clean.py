from kafka import KafkaConsumer, KafkaProducer
#from kafka import NoBrokersAvailable
from json import loads
from time import sleep
import os
       
kafka_topic = 'raw' 
while True:
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
        )

        if __name__ == "__main__":
            print("CLEAN")
            for message in clean_consumer:
                #value='25/1700859867.9161658/temperature'
                tmessage = message.value.split("/")
                print(message)
                topic = tmessage[2]
                value = int(tmessage[0])
                if topic == "temperature" and value >= -18 and value <= 28:
                    clean_producer.send("clean", message)
                    

    except: #NoBrokersAvailable
        sleep(1)
        pass