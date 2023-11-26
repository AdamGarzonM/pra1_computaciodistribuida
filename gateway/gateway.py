import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer
from json import dumps
from os import environ

# Configuració del productor de Kafka
kafka_producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    api_version=(0,11,5),
    max_in_flight_requests_per_connection = 1
)

def on_message(client, userdata, msg):
    data = msg.payload.decode() + "/" + broker
    print(f"Gateway received payload: {data}")
    kafka_producer.send("raw", data)

if __name__ == "__main__":
    broker = environ.get("BROKER")
    port = int(environ.get("PORT"))
    print(f"Gateway amb Broker {broker} with port {port}")
    subscribe.callback(on_message, f"Gateway/{broker}/+", hostname="host.docker.internal", port=port)

