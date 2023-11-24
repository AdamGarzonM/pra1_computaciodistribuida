import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer, KafkaConsumer
from json import dumps

# Configuració del productor de Kafka
kafka_producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda x: dumps(x)
)


def on_message(client, userdata, msg):
    data = msg.payload.decode()
    data_parts = data.split('/')
    data_kind = data_parts[2]
    data = data_parts[0] + data_parts[1]

    kafka_producer.send(data_kind, data)

if __name__ == "__main__":
    broker = "albert_mqtt"
    subscribe.callback(on_message, "Gateway/{broker}/+", hostname="host.docker.internal")
