from kafka import KafkaConsumer
#from kafka import NoBrokersAvailable
from json import loads
from time import sleep
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

db_user = os.environ.get("DOCKER_INFLUXDB_INIT_USERNAME")
db_pass = os.environ.get("DOCKER_INFLUXDB_INIT_PASSWORD")
db_org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
db_bucket = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
db_token = os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
db_hostname = os.environ.get("DOCKER_INFLUXDB_HOSTNAME")
db_port = os.environ.get("DOCKER_INFLUXDB_PORT")

raw_topic = 'raw' 
clean_topic = 'clean'
while True:
    try:
        raw_save_consumer = KafkaConsumer(
            raw_topic,
            bootstrap_servers = ['kafka : 9092'],
            group_id = 'save_service',
            auto_offset_reset = 'latest',
            enable_auto_commit = True,
            value_deserializer = lambda x: loads(x.decode('utf-8'))
        )

        clean_save_consumer = KafkaConsumer(
            clean_topic,
            bootstrap_servers = ['kafka : 9092'],
            group_id = 'save_service_clean',
            auto_offset_reset = 'latest',
            enable_auto_commit = True,
            value_deserializer = lambda x: loads(x.decode('utf-8'))
        )

        if __name__ == "__main__":
            print("SAVE")
            for message in raw_save_consumer:
            #for msg , message in zip(raw_save_consumer, clean_save_consumer):
                #value='25/1700859867.9161658/temperature'
                #message = message.value.split("/")
                #print(f"SAVE_RAW recieved message: {msg}")
                print(f"SAVE_CLEAN recieved message: {message}")
    except: #NoBrokersAvailable
        sleep(1)
        pass