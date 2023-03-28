import cv2
import depthai as dai
import numpy as np
import time 
import socket


# Create pipeline
pipeline = dai.Pipeline()

# Define camera nodes
color_cam = pipeline.createColorCamera()
#color_cam.setPreviewSize(1280, 720)
color_cam.setPreviewSize(1920, 1080)


color_cam.setInterleaved(False)
color_cam.initialControl.setManualFocus(0)

# Set manual exposure and initial exposure time
exposure_time_us = 10000
iso_value = 400
color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

# Define output nodes
xout = pipeline.createXLinkOut()
xout.setStreamName("color")

# Link nodes
color_cam.preview.link(xout.input)

# Create device and start pipeline
device = dai.Device(pipeline)
queue = device.getOutputQueue("color", maxSize=4, blocking=False)



# #def server_program():
# # get the hostname
# host = "192.168.0.2"
# port = 50000  # initiate port no above 1024

# server_socket = socket.socket()  # get instance
# # look closely. The bind() function takes tuple as argument
# server_socket.bind((host, port))  # bind host address and port together

# # configure how many client the server can listen simultaneously
# server_socket.listen(1)
# ur10, address = server_socket.accept()  # accept new connection
# #print("Connection from: " + str(address))

# # receive data stream. it won't accept data packet greater than 1024 bytes
# data = ur10.recv(1024).decode()
# print(str(data))
# # ur10.send(data.encode())  # send data to the client



HOST = "192.168.0.2" # The remote host
PORT = 30002 # The same port as used by the server

print("Starting Program")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
time.sleep(0.5)

# print("Set output 1 and 2 high")

# s.send("set_digital_out(1,True)\n".encode())
# time.sleep(0.1)

# s.send("set_digital_out(2,False)" + "\n")
# time.sleep(2)

print("Robot starts Moving to 3 positions based on joint positions")

#s.send("movej(p[-0.06, -0.72, 0.03, 3.1, 0, 0], a=0.5, v=0.25)\n".encode())
#time.sleep(10)
do = True

# Main loop
while True:
    in_frame = queue.get()
    image = in_frame.getCvFrame()
    image = image[0:1080, 200:1725]
    gray_belt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_belt, 150, 255, cv2.THRESH_BINARY)

    # Detect the objects
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:

        # Calculate area & Perimeter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        # Calculate approximate polygonal curve
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        #pixel_cm_ratio = 10 / 1.2 # HD
        pixel_cm_ratio = 10 / 0.8 # FHD
        # Get Width and Height of the Objects by applying the Ratio pixel to cm
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio

        # Draw contour and polygon on original image
        if area > 5000:
            cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
            #print(int(x), int(y))
            #cv2.rectangle((image, 20,20, (200,200), 5, (0, 0, 255), -1))
            cv2.polylines(image, [box], True, (255, 0, 0), 2)
            cv2.putText(image, "Width {:.2f} cm".format(object_width, 0), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "Height {:.2f} cm".format(object_height, 0), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "X {:.2f} CM".format(x/pixel_cm_ratio), (int(x - 40), int(y -35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "Y {:.2f} CM".format(y/pixel_cm_ratio), (int(x - 40), int(y + 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            new = -0.135 - (x/10)
            new = new/100
            while do :
                s.send("movej(p[0.4, -0.999, 0.03, 3.1, 0, 0], a=0.5, v=0.25)\n".encode())
                print(new)
                do= False




            # # Bottom Left corner
            
            # # # Bottom Right corner 
            # cv2.circle(image, (1287, 895), 5, (0, 255, 0), -1)
            # # # Top Right corner 
            # cv2.circle(image, (1250, 198), 5, (0, 255, 0), -1)
            # # # Top Left corner
            # cv2.circle(image, (237 , 182), 5, (0, 255, 0), -1)
            # cv2.circle(image, (933, 701), 5, (0, 255, 0), -1)

        #cv2.circle(image, (1, 1), 5, (0, 255, 0), -1)
        start_time = time.time()
        cv2.imshow("Frame", image)
        end_time = time.time()
        detection_time = end_time - start_time
        #print(detection_time)
    

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

