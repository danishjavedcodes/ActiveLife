import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

interpreter = tf.lite.Interpreter(model_path='lite-model_movenet_singlepose_lightning_3.tflite')
interpreter.allocate_tensors()
sensitivity = 30
axis = []
import pyautogui
from time import sleep
pyautogui.FAILSAFE = True
screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
screenWidth, screenHeight


def save_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold and all(kp == shaped[0]):
            cv2.circle(frame, (int(kx), int(ky)), 4, (255,0,0), -1) # Blue circle for head
            # print("Head: ", ' Y ', kp[0], ' X ', kp[1], ' c ', kp[2])
            # Y = kp[0]
            # X = kp[1]
            axis.append(kp[0])
            axis.append(kp[1])

            # print(f"Y = {axis[0]}, X = {axis[1]}")





def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold and all(kp == shaped[0]):
            cv2.circle(frame, (int(kx), int(ky)), 4, (255,0,0), -1) # Blue circle for head
            # print(f"Initial:  Y = {axis[0]}, X = {axis[1]}")
            # print("Head: ", ' Y ', kp[0], ' X ', kp[1])
            
            #Detects ups and downs
            if kp[0] > axis[0]+sensitivity:
                # print("Down")
                pyautogui.press('down')
            elif kp[0] < axis[0]-(sensitivity-20):
                # print("Up")
                pyautogui.press('up')
            # else:
                # print("No Change")
            
            #Detects rignt and lefts
            if kp[1] > axis[1]+sensitivity:
                # print("left")
                axis[1] = kp[1]
                pyautogui.press('left')
            elif kp[1] < axis[1]-sensitivity:
                axis[1] = kp[1]
                # print("right")
                pyautogui.press('right')
            # else:
                # print("No Change")




confidence_threshold = 0.4
# i = 0
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    # i = 0
    # Reshape image
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192,192)
    input_image = tf.cast(img, dtype=tf.float32)
    
    # Setup input and output 
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Make predictions 
    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    save_keypoints(frame, keypoints_with_scores, confidence_threshold)
    # print(f"X = {axis[0]}, Y = {axis[1]}")
    #get initial points
    # if i==0:
        # save_keypoints(frame, keypoints_with_scores, confidence_threshold)
        # print(f"X = {axis[0]}, Y = {axis[1]}")
        # i = 1
    # Rendering 


    draw_keypoints(frame, keypoints_with_scores, confidence_threshold)   
    
    # cv2.imshow('MoveNet Lightning', frame)
    
    # if cv2.waitKey(5) & 0xFF==ord('q'):
    #     break
        
cap.release()
cv2.destroyAllWindows()