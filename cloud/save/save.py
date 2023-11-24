from kafka import KafkaConsumer
from json import loads
from time import sleep

kafka_topic = 'topic' 

save_consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers = ['kafka : 9092'],
    group_id = 'save_service',
    auto_offset_reset = 'latest',
    enable_auto_commit = True,
    value_deserializer = lambda x: loads(x.decode('utf-8'))
)



if __name__ == "__main__":
    print("SAVE")
    for message in save_consumer:
        #message = message.value
        print(f"SAVE recieved message: {message}")
    