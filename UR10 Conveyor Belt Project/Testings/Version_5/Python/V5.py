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
exposure_time_us = 8000
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




def get_encoder_count(encoder_count_deque):
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

        # receive data stream. it won't accept data packet greater than 1024 bytes
        Encoder_count = UR10.recv(1024).decode()
        #print(Encoder_count)
        encoder_count_deque.append(Encoder_count)
        #print("-",Encoder_count)

# # ###############################################################################

encoder_count_deque = deque()

t1 = threading.Thread(target=get_encoder_count, args=(encoder_count_deque,))
t1.start()

def send_encoder(encoder_count_deque, POS_Y_queue, target_encoder):
    host = ""
    port = 50000  # initiate port no above 1024

    continue_running = True
    while continue_running:
        UR10_Encoder_socket = socket.socket()  # get instance
        UR10_Encoder_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set SO_REUSEADDR option
        UR10_Encoder_socket.bind((host, port))  # bind host address and port together
        UR10_Encoder_socket.listen(1)
        UR10_Encoder, address = UR10_Encoder_socket.accept()  # accept new connection

        POS_Y = POS_Y_queue.get()
        PosLoc = [POS_Y, target_encoder]

        encoded_data = '({:.15f},{:.15f})'.format(PosLoc[0], PosLoc[1]).encode()

        UR10_Encoder.send(encoded_data)
        data = UR10_Encoder.recv(1024).decode()
        print(str(data))

        # Close the connection after sending the target encoder
        UR10_Encoder.close()
        UR10_Encoder_socket.close()

        # Set the flag to False to end the thread
        continue_running = False
        break



POS_Y_queue = queue.Queue()

conveyor_speed_deque = deque()
optimal_distance_deque = deque(maxlen=10)  # Initialize a deque with a maximum length of 10

def speed(optimal_distance_deque):
    # get the hostname
    host = ""
    port = 50002  # initiate port no above 1024

    Speed_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    Speed_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
    Speed_socket.listen(1)
    UR10, address = Speed_socket.accept()  # accept new connection
    #print("Connection from: " + str(address))
    while True: 
        # receive data stream. it won't accept data packet greater than 1024 bytes
        Conveyor_Speed = UR10.recv(1024).decode()
        print(Conveyor_Speed)
        conveyor_speed_deque.append(Conveyor_Speed)
        
        # Calculate the optimal distance based on the conveyor speed
        speed = float(Conveyor_Speed)
        if speed > 0 and speed <= 10:
            optimal_distance = 20450
        elif speed > 10 and speed <= 20:
            optimal_distance = 20425
        elif speed > 20 and speed <= 30:
            optimal_distance = 20400
        elif speed > 30 and speed <= 40:
            optimal_distance = 20200
        elif speed > 40 and speed <= 50:
            optimal_distance = 20100
        elif speed > 50 and speed <= 60:
            optimal_distance = 19950
        elif speed > 60 and speed <= 70:
            optimal_distance = 19700
        elif speed > 70 and speed <= 82:
            optimal_distance = 19560
        elif speed > 82 and speed <= 92:
            optimal_distance = 19500
        elif speed > 92 and speed <= 100:
            optimal_distance = 19600
        else:
            optimal_distance = None  # Handle invalid speed values3

        # Append the calculated optimal distance to the deque
        print(optimal_distance)
        optimal_distance_deque.append(optimal_distance)




t3 = threading.Thread(target=speed, args=(optimal_distance_deque,))
t3.start()

def Boolean(stored_x, POS_Y_queue, optimal_distance_deque):
    if len(optimal_distance_deque) > 0:  # check if there are new values in the deque
        optimal_distance = optimal_distance_deque.pop()
        
    else:
        optimal_distance = None  # Handle the case where the deque is empty

    if len(encoder_count_deque) > 0:  # check if there are new values in the deque
        encoder_count_str = encoder_count_deque.pop()
        encoder_count = float(encoder_count_str)
        target_encoder = encoder_count + optimal_distance
        
        robot_ip = '192.168.0.2'  # replace with the IP address of your robot
        robot_port = 30002
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((robot_ip, robot_port))
    
        secondary_program = 'sec secondaryProgram():\n  set_digital_out(3, True)\nend\n'
        sock.send(secondary_program.encode())

        t2 = threading.Thread(target=send_encoder, args=(encoder_count_deque, POS_Y_queue, target_encoder))
        t2.start()

        # close the TCP/IP connection
        sock.close()






# Define a threshold for the y-coordinate
y_threshold = 100
t4 = None

code_executed = False


prev_x = None
prev_y = None
prev_time = time.time()


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
        start_point = (0, 900)
        end_point = (1920, 900)
        color = (0, 0, 255)
        thickness = 2
        cv2.line(image, start_point, end_point, color, thickness)
        # Draw contour and polygon on original image
        if area > 30000 and area < 47000:
            #print("--------------------------------------------------------------------------")
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
        if prev_x is not None and prev_y is not None:
            # Calculate the distance traveled by the object
            dx = (current_x - prev_x) / pixel_cm_ratio
            dy = (current_y - prev_y) / pixel_cm_ratio
            distance = np.sqrt(dx**2 + dy**2)

            # Calculate the time taken
            current_time = time.time()
            time_diff = current_time - prev_time

            # Calculate the speed
            speed = distance / time_diff
            #if current_y > 900 :
            # Print the speed
            #print(f"Speed: {speed:.2f} cm/s")

        # Update the previous position and time
        prev_x = current_x
        prev_y = current_y
        prev_time = time.time()
    if stored_x is not None :#and not encoder_count_queue.empty():
        # Encoder_count = encoder_count_queue.get()
        # Target_Encoder = Encoder_count + 17472
        POS_Y_0 = 135.30
        if stored_x is not None:
            X_ur10 = (stored_x/pixel_cm_ratio)*10
            POS_Y = -1 * (X_ur10 + POS_Y_0)
           


    if stored_x is not None and not code_executed:
        if current_y is not None and current_y <= 900:  
            print("y ==== ", current_y)  
            t4 = threading.Thread(target=Boolean, args=(stored_x, POS_Y_queue, optimal_distance_deque,))
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
