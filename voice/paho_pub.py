import paho.mqtt.client as mqtt
sender = mqtt.Client("sender")
sender.connect("192.168.0.107")
while True:
    sender.publish("meow", input("Message? "))
