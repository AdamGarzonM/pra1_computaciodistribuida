import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer
from json import dumps
import os

# Configuració del productor de Kafka
kafka_producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    api_version=(0,11,5), # no se si es necessari
    max_in_flight_requests_per_connection = 1
)

def on_message(client, userdata, msg):
    data = msg.payload.decode() + "/" + broker
    print(f"Gateway received payload: {data}")
    # data_parts = data.split('/')
    # data_kind = data_parts[2]
    #data = data_parts[0] + "/" + data_parts[1]
    #kafka_producer.send(data_kind, data)
    kafka_producer.send("raw", data) #TODO: topic

if __name__ == "__main__":
    broker = os.environ.get("BROKER")
    port = int(os.environ.get("PORT"))
    #broker = "albert_mqtt"
    print(f"Gateway amb Broker {broker} with port {port}")
    subscribe.callback(on_message, f"Gateway/{broker}/+", hostname="host.docker.internal", port=port)

