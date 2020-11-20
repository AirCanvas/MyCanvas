import numpy as np
import cv2 as cv
from collections import deque

# callback function to be passed in trackbar


def nothing(x):
    pass


# The trackbars needed for adjusting the marker colour
cv.namedWindow("Color detectors")
cv.createTrackbar("Upper Hue", "Color detectors", 153, 180, nothing)
cv.createTrackbar("Upper Saturation", "Color detectors", 255, 255, nothing)
cv.createTrackbar("Upper Value", "Color detectors", 255, 255, nothing)
cv.createTrackbar("Lower Hue", "Color detectors", 64, 180, nothing)
cv.createTrackbar("Lower Saturation", "Color detectors", 72, 255, nothing)
cv.createTrackbar("Lower Value", "Color detectors", 49, 255, nothing)

# array to handle colour blue_points
blue_points = [deque(maxlen=1024)]

# This index will be used to mark the blue_points in particular arrays
blue_index = 0


# Command to access video from webcam
cap = cv.VideoCapture(0)

# keep looping
while True:
    # Reading the frame from the camera
    isTrue, frame = cap.read()
    # Flipping the frame to see same side as that of user
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Getting the various HSV values
    u_hue = cv.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv.getTrackbarPos("Lower Value", "Color detectors")

    Upper_hsv = np.array([u_hue, u_saturation, u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])

    # The kernel to be used for dilation purpose
    kernel = np.ones((5, 5), np.uint8)
    # Identifying the pointer by creating the mask
    Mask = cv.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv.erode(Mask, kernel, iterations=1)
    Mask = cv.morphologyEx(Mask, cv.MORPH_OPEN, kernel)
    Mask = cv.dilate(Mask, kernel, iterations=1)

    # Find contours for the pointer after identifying it
    cnts, hierarchy = cv.findContours(Mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    center = None

    # Ifthe contours are formed
    if len(cnts) > 0:
        # sorting the contours to find biggest
        cnt = sorted(cnts, key=cv.contourArea, reverse=True)[0]
        # Getting the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), -1)
        # Calculating the center of the detected contour
        M = cv.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        blue_points[blue_index].appendleft(center)

    # Append the next deques when nothing is detected to avoid formation of straight lines
    else:
        blue_points.append(deque(maxlen=1024))
        blue_index += 1

    # Draw lines on the canvas and the frame
    colors = (255, 0, 0)
    for i in range(len(blue_points)):
        for j in range(1, len(blue_points[i])):
            if blue_points[i][j - 1] is None or blue_points[i][j] is None:
                continue
            cv.line(frame, blue_points[i][j - 1], blue_points[i][j], colors, 2)

    # Show the windows
    cv.imshow("Main frame", frame)
    cv.imshow("mask", Mask)

    # If the 'q' key is pressed then stop the application
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all the windows
cap.release()
cv.destroyAllWindows()
