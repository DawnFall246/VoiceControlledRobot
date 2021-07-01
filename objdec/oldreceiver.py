import paho.mqtt.client as mqtt #import the client1
import time
import Robot
############
def on_message(client, userdata, message):
    print("That's right!")
    robot = Robot.Robot(left_trim=10,right_trim=0)
    message = str(message.payload.decode("utf-8"))
    if message == 'forward':
       robot.forward(50,3.0)
    elif message == 'backward':
       robot.backward(50,3.0)
    elif message == 'clockwise':
       robot.right(50,3.0)
    elif message == 'counterclockwise':
       robot.left(50,3.0)
    elif message == 'dance':
       robot.forward(50,3.0)
       robot.backward(50,3.0)
       robot.backward(150,0.5)
       robot.forward(50,3.0)
       robot.right(50,3.0)
       robot.left(50,3.0)
       robot.right(50,3.0)
       robot.right(150,2.0)
       robot.left(50,3.0)
       robot.forward(100,1.0)
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
#broker_address="192.168.137.222"
broker_address="localhost"
receiver = mqtt.Client("receiver") #create new instance
receiver.on_message=on_message #attach function to callback
receiver.connect(broker_address) #connect to broker
#receiver.loop_start() #start the loop
receiver.subscribe("robot")
while True:
    receiver.loop()
