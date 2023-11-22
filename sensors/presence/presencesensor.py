#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.client as paho
import time
import random

#hostname
broker="albert_mqtt"
#port
port=1883

def on_publish(client,userdata,result):
    print("Device 1 : Data published.")
    pass

client = paho.Client("admin")
client.on_publish = on_publish
client.connect(broker,port)

for i in range(20):
    message = random.randint(0,1)
    
    time.sleep(4)
    ret = client.publish("/data",message)
    