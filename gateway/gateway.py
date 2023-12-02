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
    #data = msg.payload.decode() + "/" + broker
    data = msg.payload.decode()
    print(f"Gateway received payload: {data} from topic {msg.topic}")
    _, _, component = data.split("/")
    data = data + "/" + broker
    print(component)
    if component == "lightbulb" or component == "heatpump":
        print(f"Gateway sent payload: {data} into topic clean")
        kafka_producer.send("clean", data)
    else: 
        print(f"Gateway sent payload: {data} into topic raw")
        kafka_producer.send("raw", data)

if __name__ == "__main__":
    broker = environ.get("BROKER")
    port = int(environ.get("PORT"))
    print(f"Gateway amb Broker {broker} with port {port}")
    subscribe.callback(on_message, f"Gateway/{broker}/+", hostname="host.docker.internal", port=port)

