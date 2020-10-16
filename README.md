# MyCanvas


This is a basic project based on computer vision made in OpenCV Python which enables the user to draw on their system screen by drawing in
air with a target, preferably the tips of your finger, which is tracked by the computer webcam. The aim is to track the target first, and then its motion
and be able to replicate its path on the screen. 
This is done using OPENCV filters like Gaussian blur. The location of the target is tracked , the image is masked and the centre of the target is calculated.
Then the path of the centre of the target is drawn on the screen.

This is the basic idea of what is planned to be done.Some other features to be added will include a colour palette, and other features of a classic Paint 
application. The scope for other improvements could include incorporating a model to interpret what is written, atleast numbers.

The intention of this project was to get familiar with OpenCV, and learn how filters in OpenCV work.
