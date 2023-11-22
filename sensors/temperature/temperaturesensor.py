#simulator device 1 for mqtt message publishingimport paho.mqtt.client as paho
import paho.mqtt.client as paho
import time
import random

#hostname
broker="albert_mqtt"
#port
port=1883

def on_publish(client,userdata,result):
    print("Device 2 : Data published.")
    pass

print("ADASDASDASDASDASDD")
client = paho.Client("admin")
client.on_publish = on_publish
print(client)
client.connect(broker,port)

for i in range(20):
    message = random.randint(-20,70)
    print("ADASDASDASDASDASDASDASDASDASDAS")
    #telemetry to send 
    #message = "Device 1 : Data " + d
    time.sleep(3)
    ret = client.publish("/data",message)
    #print(ret)
    