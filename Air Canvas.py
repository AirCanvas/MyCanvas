from _collections import deque
import cv2 as cv
import numpy as np


#######################################################################################
## FUNCTIONS ##
#######################################################################################

def empty(a):
    pass


## Used to get the desired colour.
def colour_picker():
    ## Creating a window called Trackbars in order to get the desired values to mask ##
    ## Values obtained in the trackbars are then hardcoded to detect the desired colour. ##
    cv.namedWindow("TrackBars")
    cv.resizeWindow("TrackBars", 640, 240)
    cv.createTrackbar("Hue Min", "TrackBars", 41, 179, empty)
    cv.createTrackbar("Hue Max", "TrackBars", 100, 255, empty)
    cv.createTrackbar("Sat Min", "TrackBars", 54, 255, empty)
    cv.createTrackbar("Sat Max", "TrackBars", 177, 255, empty)
    cv.createTrackbar("Val Min", "TrackBars", 67, 255, empty)
    cv.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

    ## Opening the camera using device '0' i.e in-built camera.
    cap = cv.VideoCapture(0)

    ##  Looping while True where we read framewise, flip the frame to get desired directional motion.
    while True:
        # img=cv.imread("Resources/Screenshot 2020-09-21 112519.png")
        ret, img = cap.read()
        img = cv.flip(img, 1)

        ## Resize the image
        img2 = cv.resize(img, (500, 400))
        ##Convert the image to HSV  (hue, saturation, value, also known as HSB or hue, saturation, brightness).
        imgHSV = cv.cvtColor(img2, cv.COLOR_BGR2HSV)

        ## Getting the values from the trackbars that were adjusted.
        h_min = cv.getTrackbarPos("Hue Min", "TrackBars")
        h_max = cv.getTrackbarPos("Hue Max", "TrackBars")
        s_min = cv.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv.getTrackbarPos("Sat Max", "TrackBars")
        v_min = cv.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv.getTrackbarPos("Val Max", "TrackBars")

        ## Making an array of all the minimum values for h, s and v.
        lower = np.array([h_min, s_min, v_min])
        ## Making an array of all the maximum values for h, s and v.
        upper = np.array([h_max, s_max, v_max])

        ## Print in each iteration to debug.
        ##print(h_min,h_max,s_min,s_max,v_min,v_max)

        ## Create a mask for the frame from the values obtained from the trackbar positions.
        mask = cv.inRange(imgHSV, lower, upper)

        ## Making a new variable to store the bitwise AND of the image with itself applying the mask.
        imgNew = cv.bitwise_and(img2, img2, mask=mask)

        ## Show both the image and masked image.
        cv.imshow("mask", imgNew)
        cv.imshow("Out", img2)
        ##Delay of 1 ns
        cv.waitKey(1)

        ##If 'q' is pressed, loop breaks and operation stops.
        if (cv.waitKey(1) & 0xFF == ord('q')):
            break


#########################################################################################


# Define the upper and lower boundaries for a color to be considered. Currently red.
# Can be changed later with the detector function which will be added.
Lower_red = np.array([161, 155, 84])
Upper_red = np.array([179, 255, 255])

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

colorIndex = 0

## Create a window which will act as the canvas.
paintWindow = np.zeros((471, 636, 3)) + 255
cv.putText(paintWindow, "DRAW HERE BRO!", (208, 33), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)
cv.imshow("Canvas", paintWindow)

# Load the video
camera = cv.VideoCapture(0)

# Keep looping throught the frames.
while True:
    # Grab the current frame and flip it to get desired direction of stylus
    (grabbed, frame) = camera.read()
    frame = cv.flip(frame, 1)

    # Check to see if we have reached the end of the video (useful when input is a video file not a live video stream)
    if not grabbed:
        break

    ## Draw the colour palette on the left hand side.
    ## Open to editing and reshaping as well as alignment.
    frame = cv.rectangle(frame, (565 - 40, 5), (605 - 40, 45), (0, 0, 0), 1)
    frame = cv.rectangle(frame, (625 - 40, 5), (665 - 40, 45), colors[0], -1)
    frame = cv.rectangle(frame, (565 - 40, 65), (605 - 40, 105), colors[1], -1)
    frame = cv.rectangle(frame, (625 - 40, 65), (665 - 40, 105), colors[3], -1)
    frame = cv.rectangle(frame, (565 - 40, 125), (605 - 40, 165), colors[2], -1)

    ## Colours can be named as well if desired.
    # cv.putText(frame, "CLEAR ALL", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)
    # cv.putText(frame, "BLUE", (185, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    # cv.putText(frame, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    # cv.putText(frame, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    # cv.putText(frame, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1, cv.LINE_AA)

    ## Show each frame until 'q' is clicked.
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

