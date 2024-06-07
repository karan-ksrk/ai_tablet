import cv2 as cv
import numpy as np



im_src = cv.imread("new_scenery.jpg")


cap = cv.VideoCapture(0)


aruco_square_ids = [92, 920, 921, 922]

def main():
    while cv.waitKey(1) < 0:
        try:
            # get frame from the video
            hasFrame, frame = cap.read()


            #Load the dictionary that was used to generate the markers.
            dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_1000)
            
            # Initialize the detector parameters using default values
            parameters =  cv.aruco.DetectorParameters()
            
            # Detect the markers in the image
            markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)

            index = np.squeeze(np.where(markerIds==aruco_square_ids[0]))
            refPt1 = np.squeeze(markerCorners[index[0]])[0]
            
            index = np.squeeze(np.where(markerIds==aruco_square_ids[1]))
            refPt2 = np.squeeze(markerCorners[index[0]])[0]

            distance = np.linalg.norm(refPt1-refPt2)
            
            scalingFac = 0.02
            pts_dst = [[refPt1[0] - round(scalingFac*distance), refPt1[1] - round(scalingFac*distance)]]
            pts_dst = pts_dst + [[refPt2[0] + round(scalingFac*distance), refPt2[1] - round(scalingFac*distance)]]
            
            index = np.squeeze(np.where(markerIds==aruco_square_ids[2]))
            refPt3 = np.squeeze(markerCorners[index[0]])[0]
            pts_dst = pts_dst + [[refPt3[0] + round(scalingFac*distance), refPt3[1] + round(scalingFac*distance)]]

            index = np.squeeze(np.where(markerIds==aruco_square_ids[3]))
            refPt4 = np.squeeze(markerCorners[index[0]])[0]
            pts_dst = pts_dst + [[refPt4[0] - round(scalingFac*distance), refPt4[1] + round(scalingFac*distance)]]

            pts_src = [[0,0], [im_src.shape[1], 0], [im_src.shape[1], im_src.shape[0]], [0, im_src.shape[0]]]
            
            pts_src_m = np.asarray(pts_src)
            pts_dst_m = np.asarray(pts_dst)

            # Calculate Homography
            h, status = cv.findHomography(pts_src_m, pts_dst_m)
            
            # Warp source image to destination based on homography
            warped_image = cv.warpPerspective(im_src, h, (frame.shape[1],frame.shape[0]))
            
            # Prepare a mask representing region to copy from the warped image into the original frame.
            mask = np.zeros([frame.shape[0], frame.shape[1]], dtype=np.uint8)
            cv.fillConvexPoly(mask, np.int32([pts_dst_m]), (255, 255, 255), cv.LINE_AA)

            # Erode the mask to not copy the boundary effects from the warping
            element = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
            mask = cv.erode(mask, element, iterations=3)

            # Copy the mask into 3 channels.
            warped_image = warped_image.astype(float)
            mask3 = np.zeros_like(warped_image)
            for i in range(0, 3):
                mask3[:,:,i] = mask/255

            # Copy the warped image into the original frame in the mask region.
            warped_image_masked = cv.multiply(warped_image, mask3)
            frame_masked = cv.multiply(frame.astype(float), 1-mask3)
            im_out = cv.add(warped_image_masked, frame_masked)
            
            # Showing the original image and the new output image side by side
            # concatenatedOutput = cv.hconcat([frame.astype(float), im_out])
            cv.imshow("AR using Aruco markers", im_out.astype(np.uint8))


        except Exception as inst:
            print(inst)
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()