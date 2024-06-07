import cv2
import numpy as np

def find_tab(frame):
    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Apply Gaussian blur and Canny edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)

    frame_copy = frame.copy()
    cv2.drawContours(image=frame_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)

    # for contour in contours:
    #     # Approximate the contour to a polygon
    #     cv2.fillPoly(frame_copy, pts=contour, color=(0, 0, 255))

    return frame_copy


def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        frame = find_tab(frame)
        
        cv2.imshow("Image", cv2.resize(frame, (960, 540)))
        k = cv2.waitKey(1)
        
        if k%256 == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()