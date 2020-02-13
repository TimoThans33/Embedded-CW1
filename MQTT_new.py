import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("broker.hivemq.com", 1883)
client.loop_start()

#while True:
#    temperature = 123456
#    (rc, mid) = client.publish("imperialspinal", str(temperature), qos=1)
#    time.sleep(30)
