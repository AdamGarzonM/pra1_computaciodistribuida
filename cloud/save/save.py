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

kafka_topic = 'topic' 
while True:
    try:
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
            influxToken = "s2d3rf67ren42i0gg666er9"
            for message in save_consumer:
                #value='25/1700859867.9161658/temperature'
                message = message.value.split("/")
                print(f"SAVE recieved message: {message}")
    except: #NoBrokersAvailable
        sleep(1)
        pass