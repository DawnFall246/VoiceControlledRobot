import paho.mqtt.client as mqtt #import the client1
from robotfinder import *
import time
import Robot
############
def on_message(client, userdata, message):
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
    elif message.startswith('find'):
       for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

           frame = np.copy(frame1.array)
           frame.setflags(write=1)
           frame_expanded = np.expand_dims(frame, axis=0)

           # Perform the actual detection by running the model with the image as input
           (boxes, scores, classes, num) = sess.run(
               [detection_boxes, detection_scores, detection_classes, num_detections],
               feed_dict={image_tensor: frame_expanded})

           class_list = list(np.squeeze(classes).astype(np.int32))
           scores_list = list(np.squeeze(scores))
           found = False
           for i in range(len(class_list)):
               if scores_list[i] >= 0.5:
                   #print(i, class_list[i], scores_list[i])
                   if class_list[i] in category_index:
                       if category_index[class_list[i]]['name'] == message[5 :]:
                           print(message[5 :])
                           robot.stop()
                           found = True
                           break

           if not found:
               robot.left(100,0.5)
           else:
               break

           rawCapture.truncate(0)

       camera.close()

       cv2.destroyAllWindows()
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
broker_address="192.168.137.222"
#broker_address="192.168.0.107"
receiver = mqtt.Client("receiver") #create new instance
receiver.on_message=on_message #attach function to callback
receiver.connect(broker_address) #connect to broker
#receiver.loop_start() #start the loop
receiver.subscribe("robot")
while True:
    receiver.loop()
