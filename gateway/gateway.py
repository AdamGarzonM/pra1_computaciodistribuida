import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer, KafkaConsumer
from json import dumps

# Configuració del productor de Kafka
kafka_producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# Configuració del consumidor de Kafka per al microservei "Actuation"
consumer_conf = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'actuation_service',
    'auto.offset.reset': 'earliest',
}

actuation_consumer = KafkaConsumer(consumer_conf)

kafka_topic = 'param_topic'  # Utilitza el mateix tema al qual es subscriu l'altre microservei
actuation_consumer.subscribe([kafka_topic])

def actuate():
    try:
        while True:            
            parameters = "coses que pillem de influxdb"
            should_actuate = decide_actuation(parameters)
            if should_actuate and data_kind == "temperature":
                # mqtt a heat pump
                print("a")
            if should_actuate and data_kind == "presence":
                #mqtt a lightbulb
                print("b")

    finally:
        actuation_consumer.close()

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    data_parts = data.split('/')
    data_kind = data_parts[2]
    data = data_parts[0] + data_parts[1]

    kafka_producer.send(data_kind, data)
    #ficar a influxdb

if __name__ == "__main__":
    broker = "albert_mqtt"
    subscribe.callback(on_message, "Gateway/{broker}/+", hostname="host.docker.internal")
    actuate()
