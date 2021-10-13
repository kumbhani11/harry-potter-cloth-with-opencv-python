import cv2
import time
import numpy as np
cap = cv2.VideoCapture(0)
time.sleep(2)

background = 0 # to capture background
for i in range(30):
    ret, background = cap.read()

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # hue, saturation, value
    
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red) # separating the cloak part
    
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red) 
    
    mask = mask1+mask2 # or operator
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) # noise removal
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1) # increase thickness
    mask2 = cv2.bitwise_not(mask) # except the cloak
    
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)
    final = cv2.addWeighted(res1, 1, res2, 1, 0)
    
    cv2.imshow('Display', final)
    
    if cv2.waitKey(1)==ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
