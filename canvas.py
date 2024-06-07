import numpy as np
import cv2
from collections import deque

# Variables for storing drawing points
drawing = False
ix, iy = -1, -1
frame = None  # Declare frame as a global variable
points = deque(maxlen=100)

# Function to handle mouse events
def draw(event, x, y, flags, param):
    global ix, iy, drawing, points

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        points.appendleft((x, y))  # Store the mouse position when LBUTTONDOWN event occurs

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(paintWindow, (ix, iy), (x, y), (0, 0, 0), 2)
            ix, iy = x, y
            points.appendleft((x, y))  # Store the mouse position when MOUSEMOVE event occurs

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('Paint', draw)

# Loading the default webcam of PC.
cap = cv2.VideoCapture(0)

# Keep looping
while True:
    # Reading the frame from the camera
    ret, frame = cap.read()

    # Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    
    # Draw lines based on the points deque
    for i in range(1, len(points)):
        cv2.line(frame, points[i - 1], points[i], (0, 0, 255), 2)

    # Show the tracking and paint windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    # If the 'q' key is pressed then stop the application
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()
