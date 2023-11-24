consumer_conf = {
    'bootstrap.servers': 'kafka:9092',
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