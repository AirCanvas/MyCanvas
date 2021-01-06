from _collections import deque
import cv2 as cv
import numpy as np


#######################################################################################
                                ## FUNCTIONS ##
#######################################################################################

def empty(a):
    pass

## Defining the HSV values for the blue, orange and green colour
blue_colour = [109, 114, 48, 131, 228, 113]
orange_colour = [0, 120, 118, 62, 255, 255]
green_colour = [41, 89, 94, 71, 200, 255]

## Defining the point for drawing the rectangles for palette
clear_rect = [(625 - 40, 185), (665 - 40, 225)]
blue_rect = [(625 - 40, 5), (665 - 40, 45)]
green_rect = [(625 - 40, 245), (665 - 40, 305)]
yellow_rect = [(625 - 40, 65), (665 - 40, 105)]
red_rect = [(625 - 40, 125), (655 - 40, 165)]

##Adding it to an array of colours for future expansion plans.
myColors = [blue_colour]

## Find colour function which detects the colours mentioned in the array
def findColor (img, myColors, paintcolor):
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    newPoints = []

    ## Looping through the colours defined to get a mask for each.
    for color in myColors:
        ## Making an array of all the minimum values for h, s and v.
        lower = np.array(color[0:3])
        ## Making an array of all the maximum values for h, s and v.
        upper = np.array(color[3:6])

        ## Create a mask for the frame from the values obtained from the trackbar positions.
        mask = cv.inRange(imgHSV, lower, upper)
        ## Making a new variable to store the bitwise AND of the image with itself applying the mask.
        imgNew = cv.bitwise_and(img, img, mask=mask)
        kernel = np.ones((5, 5), np.uint8)

        ##eroding and dilating the mask
        erosion = cv.erode(mask, kernel, iterations = 1)
        dilation = cv.erode(mask, kernel, iterations = 1)
        ##applying opening and closing on the mask in order to cancel out false negatives.
        opening = cv.morphologyEx( mask, cv.MORPH_OPEN, kernel)
        closing = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        x,y= getContours(closing)
        cv.circle(frame, (x,y), 10, paintcolor, cv.FILLED)
        ## If not point is detected, i.e x,y = 0,0
        if x!=0 and y!=0:
            ## If the stylus is detected over the drawn rectangles, change the paintcolour.
            if red_rect[0][0]<x<red_rect[1][0] and red_rect[0][1]<y<red_rect[1][1] :
                print("Detecting red at ", x+40, y)
                paintcolor = colors[2]
            elif blue_rect[0][0]<x<blue_rect[1][0] and blue_rect[0][1]<y<blue_rect[1][1] :
                print("Detecting blue at ", x+40, y)
                paintcolor = colors[0]
            elif yellow_rect[0][0]<x<yellow_rect[1][0] and yellow_rect[0][1]<y<yellow_rect[1][1] :
                print("Detecting yellow at ", x+40, y)
                paintcolor = colors[3]
            elif green_rect[0][0]<x<green_rect[1][0] and green_rect[0][1]<y<green_rect[1][1] :
                print("Detecting green at ", x+40, y)
                paintcolor = colors[1]
            ##append the points to newPoints
            newPoints.append([x, y, paintcolor])
        ## Show masked image.
        # cv.imshow(str(color[0]), mask)
        # cv.imshow(str(color[1]), erosion)
        # cv.imshow(str(color[2]), dilation)
        # cv.imshow("Opening", opening)
        #cv.imshow("Close", closing)

    return newPoints, paintcolor


myPoints = []  #[x , y, colorId]



## Function to get the contour of the detected masked image and draw bounding box around it
def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # print("Contours : ", contours)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 20:
            cv.drawContours(boundingFrame, cnt, -1, (255,255, 255), 3)
            peri = cv.arcLength(cnt, True)  # The 'true' here is to ensure we're detecting closed stuff
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)  # To get the corner points?
            x, y, w, h = cv.boundingRect(approx)
    return x+w//2,y ##return the tip of the detected stylus

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

##Looping through the points and drawing the points as circles.
def drawOnCanvas( myPoints):
    for point in myPoints:
        cv.circle(paintWindow,(point[0], point[1]), 10, point[2], cv.FILLED)



#########################################################################################

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

colorIndex = 0

## Create a window which will act as the canvas.
paintWindow = np.zeros((471, 636, 3)) + 255
cv.putText(paintWindow, "DRAW HERE BRO!", (208, 33), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)
cv.imshow("Canvas", paintWindow)

# Load the video
camera = cv.VideoCapture(0)
paintcolor = (0, 0, 0)
# Keep looping throught the frames.
while True:
    # Grab the current frame and flip it to get desired direction of stylus
    (grabbed, frame) = camera.read()
    frame = cv.flip(frame, 1)
    boundingFrame = frame.copy()
    # Check to see if we have reached the end of the video (useful when input is a video file not a live video stream)
    if not grabbed:
        break

    ## Draw the colour palette on the right hand side.
    ## Open to editing and reshaping as well as alignment.
    frame = cv.rectangle(frame, clear_rect[0], clear_rect[1], (0, 0, 0), 1)
    frame = cv.rectangle(frame, blue_rect[0], blue_rect[1], colors[0], 2)
    frame = cv.rectangle(frame, green_rect[0], green_rect[1], colors[1], 2)
    frame = cv.rectangle(frame, yellow_rect[0],yellow_rect[1], colors[3], 2)
    frame = cv.rectangle(frame, red_rect[0], red_rect[1], colors[2], 2)

    ## Colours can be named as well if desired.
    # cv.putText(frame, "CLEAR ALL", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)
    # cv.putText(frame, "BLUE", (185, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    # cv.putText(frame, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    # cv.putText(frame, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    # cv.putText(frame, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1, cv.LINE_AA)

    ## Show each frame until 'q' is clicked.
    new_points, paintcolor = findColor(frame, myColors, paintcolor)
    print(paintcolor)
    if len(new_points)!=0:
        for newpoint in new_points:
            myPoints.append(newpoint)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints)
    cv.imshow('frame', frame)

    cv.imshow('frameD', paintWindow)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

