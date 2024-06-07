import cv2
import cv2.aruco as aruco
import numpy as np
import os


def findArucoMarkers(img, markerSize=6, totalMarkers=1000, draw=True):
    """
    :param img: image from which markers will be detected
    :param markerSize: size of the markers
    :param totalMarkers: total number of markers
    :param draw: if true, markers will be drawn
    :return: list of detected markers
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f"DICT_{markerSize}X{markerSize}_{totalMarkers}")
    arucoDict = aruco.getPredefinedDictionary(key)
    arucoParam =  aruco.DetectorParameters()
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    
    return [bboxs, ids]



def augmentAruco(bbox, id, img, drawId=True):
    """
    :param bbox: bounding box of the marker
    :param id: id of the marker
    :param img: image on which the marker will be drawn
    :param imgAug: image of the marker
    :param drawId: if true, id will be drawn
    :return: image on which the marker has been drawn
    """
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]


    if drawId:
        cv2.putText(img, str(id), (int(tl[0]), int(tl[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
        cv2.putText(img, f"({tl[0]},{tl[1]})", (int(tl[0]), int(tl[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return img

    
def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        arucoFound = findArucoMarkers(img)

        # loop through all the markers and augment each one of them
        if len(arucoFound[0]):
            for bbox, id in zip(arucoFound[0], arucoFound[1]):
                # print(id)
                    img = augmentAruco(bbox, id, img)
        
        cv2.imshow("Image", cv2.resize(img, (960, 540)))
        k = cv2.waitKey(1)
        
        if k%256 == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()