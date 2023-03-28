import picamera
import picamera.array
import cv2
import pickle
import time 
import numpy as np


# Medium Camera resolution 
Camera_Resulution_Width = 1024
Camera_Resulution_Height = 768

# Conveyor belt dimensions
Conveyor_Belt_Width = 1024
Conveyor_Belt_Height = 768
Min_Contour_Area = 10000


with picamera.PiCamera() as camera:
    #max_res = camera.MAX_RESOLUTION
    #camera.resolution = max_res # set the camera resolution to the max resolution
    # Set the shutter speed to 1/100th of a second
    camera.shutter_speed = 3000

    # Set the ISO to 800
    camera.iso = 800

    # # Allow time for the camera to adjust to the new settings
    camera.exposure_mode = 'off'
    #camera.start_preview()
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    camera.exposure_compensation = 0
    camera.resolution = (Camera_Resulution_Width, Camera_Resulution_Height) # set the camera resolution
    #camera.framerate = 60 # set the camera framerate
    with picamera.array.PiRGBArray(camera, size=(Camera_Resulution_Width, Camera_Resulution_Height)) as output:
        
        
        # capture frames from the camera
        for frame in camera.capture_continuous(output, format='bgr', use_video_port=True):
           
            start_time = time.time()
            #convert the captured frame to an OpenCV image
            frame = frame.array
            cameraMatrix, dist = pickle.load(open("Calibration_Uni/calibration.pkl", "rb"))
            image = cv2.undistort(frame, cameraMatrix, dist, None)

            
            #image = frame.array
            #image = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            # Process the image to detect objects on the conveyor belt
            belt = image[0:Conveyor_Belt_Height, 0:Conveyor_Belt_Width]
            gray_belt = cv2.cvtColor(belt, cv2.COLOR_BGR2GRAY)
            _, threshold = cv2.threshold(gray_belt, 180, 255, cv2.THRESH_BINARY)

        # Detect the objects
            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                #(x, y, w, h) = cv2.boundingRect(cnt)
                
                # Calculate areaq
                area = cv2.contourArea(cnt)
                perimeter = cv2.arcLength(cnt, True)

                # Calculate approximate polygonal curve
                #approx = cv2.approxPolyDP(cnt, 0.01 * perimeter, True)
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect
                # Display rectangle
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                pixel_cm_ratio = 10 / 1.2
                # Get Width and Height of the Objects by applying the Ratio pixel to cm
                object_width = w / pixel_cm_ratio
                object_height = h / pixel_cm_ratio

                # Draw contour and polygon on original image
                if area > Min_Contour_Area:
                    cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(image, [box], True, (255, 0, 0), 2)
                    cv2.putText(image, "Width {} cm".format(round(object_width, 0)), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    cv2.putText(image, "Height {} cm".format(round(object_height, 0)), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
           
            #cv2.putText(image, "FPS: {:.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # display the image using OpenCV
            cv2.imshow("Frame", image)
            #cv2.imshow("Belt", threshold)
            fps = 1 / (time.time() - start_time)
            #print(h,w)
            print(fps)
            # clear the stream for the next frame
            output.truncate(0)

            # break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

cv2.destroyAllWindows()








            #cv2.putText(image, f"Detection Time: {detection_time:.4f} seconds", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
