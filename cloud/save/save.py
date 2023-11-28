from kafka import KafkaConsumer
import threading
from json import loads
from time import sleep
from os import environ
from datetime import datetime
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


db_org = environ.get("DOCKER_INFLUXDB_INIT_ORG")
db_bucket = environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
db_token = environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
db_hostname = environ.get("DOCKER_INFLUXDB_HOSTNAME")
db_port = environ.get("DOCKER_INFLUXDB_PORT")

raw_topic = 'raw' 
clean_topic = 'clean'


def prepareDbClient():
    client = InfluxDBClient(
        url = f"http://{db_hostname}:{db_port}",
        token = db_token,
        org = db_org,
    )
    twrite_api = client.write_api(write_options=SYNCHRONOUS)
    return client, twrite_api

def save_to_influxdb(message, write_api):
    source = message.topic 
    value, timestamp, data_type, broker = message.value.split("/")
    p = Point(data_type).tag("Broker", broker).tag("Source", source).field("Value", int(value)).time(datetime.fromtimestamp(int(float(timestamp))), WritePrecision.MS)
    write_api.write(bucket=db_bucket, record=p)
    print(f"SAVE has written: {p}")

def prepareConsumers():
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
        return raw_save_consumer, clean_save_consumer
    except:
        sleep(1)
        prepareConsumers()


def thread_func(raw_save_consumer):
    print("RAW_SAVE THREAD")
    for message in raw_save_consumer:
        raw_client, raw_write_api = prepareDbClient()
        save_to_influxdb(message, raw_write_api)
        raw_client.close()


if __name__ == "__main__":
    print("Starting cloud microservice SAVE")
    while True:
        try:
            raw_save_consumer, clean_save_consumer = prepareConsumers()
            break
        except TypeError as e:
            print(f"Error: {e}; because kafka is not ready, trying again...")
            sleep(2)
    
    raw_thread = threading.Thread(target=thread_func, args=(raw_save_consumer,), daemon=True)
    raw_thread.start()
    
    for message in clean_save_consumer:
        clean_client, clean_write_api = prepareDbClient()
        save_to_influxdb(message, clean_write_api)
        clean_client.close()
