import threading
import cv2
import depthai as dai
import numpy as np
import time 
import socket
import queue
from collections import deque

# Create pipeline
pipeline = dai.Pipeline()

# Define camera nodes
color_cam = pipeline.createColorCamera()
color_cam.setPreviewSize(1920, 1080)
color_cam.setInterleaved(False)
color_cam.initialControl.setManualFocus(0)

# Set manual exposure and initial exposure time
exposure_time_us = 11200
iso_value = 400
color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

# Define output nodes
xout = pipeline.createXLinkOut()
xout.setStreamName("color")

# Link nodes
color_cam.preview.link(xout.input)

# Create device and start pipeline
device = dai.Device(pipeline)
color_queue = device.getOutputQueue("color", maxSize=4, blocking=False)



global x_ur10
stored_x = None
stored_y = None



def get_encoder_count(encoder_count_queue):
    # get the hostname
    host = ""
    port = 50001  # initiate port no above 1024

    Encoder_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    Encoder_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
    Encoder_socket.listen(1)
    UR10, address = Encoder_socket.accept()  # accept new connection
    #print("Connection from: " + str(address))
    while True: 
        # if not encoder_count_queue:
        #     time.sleep(0.1)  # wait for 0.1 seconds
        #     continue  # check again
        # receive data stream. it won't accept data packet greater than 1024 bytes
        Encoder_count = UR10.recv(1024).decode()
        #print(Encoder_count)
        encoder_count_queue.put(Encoder_count)
        print("-",Encoder_count)

# # ###############################################################################

encoder_count_queue = queue.Queue()

t1 = threading.Thread(target=get_encoder_count, args=(encoder_count_queue,))
t1.start()



def send_encoder(encoder_count_queue, send_event):
    while True:
        send_event.wait()  # Wait until the event is set by the client
        host = ""
        port = 50000  # initiate port no above 1024

        UR10_Encoder_socket = socket.socket()  # get instance
        UR10_Encoder_socket.bind((host, port))  # bind host address and port together
        UR10_Encoder_socket.listen(1)
        UR10_Encoder, address = UR10_Encoder_socket.accept()  # accept new connection

        encoder_count_str = encoder_count_queue.get(block=False)
        encoder_count = float(encoder_count_str)
        Target_Encoder = encoder_count + 17702
        UR10_Encoder.send(("Target_Encoder" + str(Target_Encoder) + "\n").encode())
        print("Encoder_count:", encoder_count_str, "Target Count", Target_Encoder, "Difference", Target_Encoder - encoder_count)

        data = UR10_Encoder.recv(1024).decode()
        print(str(data))
        # Clean up the socket connection and exit the function
        UR10_Encoder.close()
        UR10_Encoder_socket.close()
        send_event.clear()  # Clear the event for the next iteration


def send_y_position(POS_Y_queue):
    host = ""
    port = 50002  # initiate port no above 1024

    UR10_Y_Position_socket = socket.socket()  # get instance
    UR10_Y_Position_socket.bind((host, port))  # bind host address and port together
    UR10_Y_Position_socket.listen(1)
    UR10_Y_Position, address = UR10_Y_Position_socket.accept()  # accept new connection

    while True:
        POS_Y = POS_Y_queue.get()
        UR10_Y_Position.send(("POS_Y " + str(POS_Y) + "\n").encode())
        data = UR10_Y_Position.recv(1024).decode()
        print(str(data))


POS_Y_queue = queue.Queue()
# t2 = threading.Thread(target=send_target_location, args=(POS_Y_queue, encoder_count_queue,))
# t2.start()

send_event = threading.Event()
t2 = threading.Thread(target=send_encoder, args=(encoder_count_queue, send_event))
t2.start()

t3 = threading.Thread(target=send_y_position, args=(POS_Y_queue,))
t3.start()



def Boolean(stored_x):
    robot_ip = '192.168.0.2'  # replace with the IP address of your robot
    robot_port = 30002
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((robot_ip, robot_port))
    secondary_program = 'sec secondaryProgram():\n  set_digital_out(3, True)\nend\n'
    sock.send(secondary_program.encode())
    # close the TCP/IP connection
    send_event.set()  # Set the event to start the send_encoder function
    sock.close()


# Define a threshold for the y-coordinate
y_threshold = 100
t4 = None

code_executed = False
# Main loop
while True:
    in_frame = color_queue.get()
    image = in_frame.getCvFrame()
    image = image[0:1080, 210:1725]
    gray_belt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray_belt_blurred = cv2.GaussianBlur(gray_belt, (5, 5), 0)
    _, threshold = cv2.threshold(gray_belt, 130, 255, cv2.THRESH_BINARY)
    
    # Detect the objects
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    object_detected = False
    # Loop through contours
    current_x = None
    current_y = None

    for cnt in contours:
        # Calculate area & Perimeter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        
        # Calculate approximate polygonal curve
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        #pixel_cm_ratio = 10 / 1.2 # HD
        pixel_cm_ratio = 10 / 0.8 # FHD
        # Get Width and Height of the Objects by applying the Ratio pixel to cm
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio

        # Draw contour and polygon on original image
        if area > 30000 and area < 37000:
            cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(image, [box], True, (255, 0, 0), 2)
            cv2.putText(image, "Width {:.2f} cm".format(object_width, 0), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "Height {:.2f} cm".format(object_height, 0), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "X {:.2f} CM".format(x/pixel_cm_ratio), (int(x - 40), int(y -35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "Y {:.2f} CM".format(y/pixel_cm_ratio), (int(x - 40), int(y + 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            current_x = x
            current_y = y
            object_detected = True
            d = y
            
    object_left_view = stored_y is not None and stored_y < y_threshold

    # Update the stored x-coordinate if the tracked object has left the camera's field of view
    if object_detected and object_left_view:
        stored_x = current_x
        stored_y = current_y
    elif object_detected and stored_x is None:
        stored_x = current_x
        stored_y = current_y
    elif object_left_view:
        stored_x = None
        stored_y = None


    # Update stored_y
    if object_detected:
        stored_y = current_y

    if stored_x is not None :#and not encoder_count_queue.empty():
        # Encoder_count = encoder_count_queue.get()
        # Target_Encoder = Encoder_count + 17472
        POS_Y_0 = 135.30
        if stored_x is not None:
            X_ur10 = (stored_x/pixel_cm_ratio)*10
            POS_Y = -1 * (X_ur10 + POS_Y_0)
           


    if stored_x is not None and not code_executed:
        t4 = threading.Thread(target=Boolean, args=(stored_x,))
        t4.start()
        POS_Y_queue.put(POS_Y)
        code_executed = True
    elif not object_detected:
        code_executed = False


    cv2.imshow("Frame", image)
    #cv2.imshow("Canny", threshold)
    

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break




