import Robot
LEFT_TRIM = 0
RIGHT_TRIM = 0
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
print("Mr. Roboto")
robot.left(100,3)

from robotfinder import *
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
                if category_index[class_list[i]]['name'] == 'cup':
                    print('cup')
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
