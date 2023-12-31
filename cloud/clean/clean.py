from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from time import sleep
       
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
            api_version=(0,11,5),
            max_in_flight_requests_per_connection = 1,
        )
        return clean_consumer, clean_producer
    except:
        sleep(1)
        prepareKafka()

if __name__ == "__main__":
    print("Starting cloud microservice CLEAN")
    while True:
        try:
            clean_consumer, clean_producer = prepareKafka()
            break
        except TypeError as e:
            print(f"Error: {e}; because kafka is not ready, trying again...")
            sleep(2)
    for message in clean_consumer: 
        value, _, topic, _ = message.value.split("/")
        value = int(value)
        if topic == "temperature" and value >= -18 and value <= 28:
            clean_producer.send("clean", value=message.value)
            print(f"CLEAN has sent {message.value}")
        elif topic == "presence" and value >= 0 and value <= 100:
            clean_producer.send("clean", value=message.value)
            print(f"CLEAN has sent {message.value}")
        else:
            print(f"CLEAN has discarded {message.value}")