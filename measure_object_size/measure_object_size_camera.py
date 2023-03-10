import cv2
from object_detector import *
import numpy as np
import picamera
import picamera.array
import pickle
import time 


Camera_Resulution_Width = 1024
Camera_Resulution_Height = 768
Conveyor_Belt_Width = 1024
Conveyor_Belt_Height = 768

Min_Contour_Area = 10000



with picamera.PiCamera() as camera:
    #max_res = camera.MAX_RESOLUTION
    #camera.resolution = max_res # set the camera resolution to the max resolution
    # Set the shutter speed to 1/100th of a second
    camera.shutter_speed = 2000

    # Set the ISO to 800
    camera.iso = 800

    # # Allow time for the camera to adjust to the new settings
    camera.exposure_mode = 'off'
    #camera.start_preview()
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    camera.exposure_compensation = 0
    camera.resolution = (Camera_Resulution_Width, Camera_Resulution_Height) # set the camera resolution
    camera.framerate = 30 # set the camera framerate
    with picamera.array.PiRGBArray(camera, size=(Camera_Resulution_Width, Camera_Resulution_Height)) as output:
        
        
        # capture frames from the camera
        for frame in camera.capture_continuous(output, format='bgr', use_video_port=True):
            

            # Load Aruco detector
            parameters = cv2.aruco.DetectorParameters_create()
            aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


            # Load Object Detector
            detector = HomogeneousBgDetector()

         

            while True:
                _, img = frame.array

                # Get Aruco marker
                corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
                if corners:

                    # Draw polygon around the marker
                    int_corners = np.int0(corners)
                    cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

                    # Aruco Perimeter
                    aruco_perimeter = cv2.arcLength(corners[0], True)

                    # Pixel to cm ratio
                    pixel_cm_ratio = aruco_perimeter / 20

                    contours = detector.detect_objects(img)

                    # Draw objects boundaries
                    for cnt in contours:
                        # Get rect
                        rect = cv2.minAreaRect(cnt)
                        (x, y), (w, h), angle = rect

                        # Get Width and Height of the Objects by applying the Ratio pixel to cm
                        object_width = w / pixel_cm_ratio
                        object_height = h / pixel_cm_ratio

                        # Display rectangle
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)

                        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                        cv2.polylines(img, [box], True, (255, 0, 0), 2)
                        cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                        cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)



                cv2.imshow("Image", img)
                key = cv2.waitKey(1)
                if key == 27:
                    break

cap.release()
cv2.destroyAllWindows()