import cv2 as cv
import numpy as np



im_src = cv.imread("new_scenery.jpg")


cap = cv.VideoCapture(0)
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_1000)
parameters =  cv.aruco.DetectorParameters()

aruco_square_ids = [92, 920, 921, 922]
opacity = 0.6
def main():
    while cv.waitKey(1) < 0:
        # Get frame from the video
        hasFrame, frame = cap.read()
        try:
            # Detect the markers in the image
            markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)

            if markerIds is not None and len(markerIds) >= 4:
                index = np.squeeze(np.where(markerIds == aruco_square_ids[0]))
                refPt1 = np.squeeze(markerCorners[index[0]])[2]

                index = np.squeeze(np.where(markerIds == aruco_square_ids[1]))
                refPt2 = np.squeeze(markerCorners[index[0]])[2]

                distance = np.linalg.norm(refPt1 - refPt2)
                scalingFac = 0.02

                pts_dst = [
                    [refPt1[0] - round(scalingFac * distance), refPt1[1] - round(scalingFac * distance)],
                    [refPt2[0] + round(scalingFac * distance), refPt2[1] - round(scalingFac * distance)]
                ]

                index = np.squeeze(np.where(markerIds == aruco_square_ids[2]))
                refPt3 = np.squeeze(markerCorners[index[0]])[2]
                pts_dst.append([refPt3[0] + round(scalingFac * distance), refPt3[1] + round(scalingFac * distance)])

                index = np.squeeze(np.where(markerIds == aruco_square_ids[3]))
                refPt4 = np.squeeze(markerCorners[index[0]])[2]
                pts_dst.append([refPt4[0] - round(scalingFac * distance), refPt4[1] + round(scalingFac * distance)])

                pts_dst_m = np.asarray(pts_dst)

                # Create a black image with the same dimensions as the frame
                black_image = np.zeros_like(frame)

                # Prepare a mask representing the region to draw black
                mask = np.zeros([frame.shape[0], frame.shape[1]], dtype=np.uint8)
                cv.fillConvexPoly(mask, np.int32([pts_dst_m]), (255, 255, 255), cv.LINE_AA)

                black_image = cv.addWeighted(black_image, opacity, frame, 1 - opacity, 0)


                # Copy the mask into 3 channels
                mask3 = np.zeros_like(frame)
                for i in range(3):
                    mask3[:, :, i] = mask

                # Draw the black region on the original frame
                black_image_masked = cv.multiply(black_image.astype(float), mask3.astype(float) / 255)
                frame_masked = cv.multiply(frame.astype(float), 1 - mask3.astype(float) / 255)
                im_out = cv.add(black_image_masked, frame_masked)

                # Convert the result to uint8
                im_out = im_out.astype(np.uint8)
            else:
                im_out = frame
            
            # Showing the original image and the new output image side by side
            # concatenatedOutput = cv.hconcat([frame.astype(float), im_out])
            cv.imshow("AR using Aruco markers", cv.resize(im_out.astype(np.uint8), (960, 540)))


        except Exception as inst:
            # print(inst)
            pass
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()