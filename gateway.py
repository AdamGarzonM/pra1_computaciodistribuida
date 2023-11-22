import paho.mqtt.client as mqtt
# This is the Subscriber
# #hostnamesdfsdf
broker = "mqtt"
#port
port = 1883
#time to live
timelive=60
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("/data")
  
def on_message(client, userdata, msg):
    data = msg.payload.decode()
    #enviar data kafka
    
client = mqtt.Client()
client.connect(broker,port,timelive)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()