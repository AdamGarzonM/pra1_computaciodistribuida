from kafka import KafkaConsumer
#from kafka import NoBrokersAvailable
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
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return client, write_api

def save_to_influxdb(message):
    source = 'raw' #TODO Aixo hauria de estar o dintre del missatge o com a depen del consumer que li envia
    #value='32/1700928523.6854231/presence/dakota_mqtt
    value, timestamp, data_type, broker = message.value.split("/")
    #broker = str(broker)
    print(f"SAVE has: {value}, {timestamp}, {data_type}, {broker}")
    p = Point(data_type).tag("Broker", broker).tag("Source", source).field("Value", int(value)).time(datetime.fromtimestamp(int(float(timestamp))), WritePrecision.MS)
    print(f"SAVE tries to write: {p}")
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

if __name__ == "__main__":
    print("SAVE")
    raw_save_consumer, clean_save_consumer = prepareConsumers()
    for message in raw_save_consumer: #aqui es llança una excepcio
    #for msg , message in zip(raw_save_consumer, clean_save_consumer):
        #value='32/1700928523.6854231/presence/dakota_mqtt
        #message = message.value.split("/")
        #print(f"SAVE_RAW recieved message: {msg}")
        print(f"SAVE recieved message: {message}")
        
        #asyncio.ensure_future(save_to_influxdb(message=message))
        client, write_api = prepareDbClient()
        save_to_influxdb(message)
        client.close()