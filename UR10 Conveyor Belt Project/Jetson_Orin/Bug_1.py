
import threading
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


def get_encoder_count():
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
    global Encoder_count
    while True: 
         
        # receive data stream. it won't accept data packet greater than 1024 bytes
        Encoder_count = UR10.recv(1024).decode()
        #print(str(Encoder_count))
        # ur10.send(data.encode())  # send data to the client

# # ###############################################################################
def send_target_location():
    # get the hostname
    host = ""
    port = 50000  # initiate port no above 1024

    UR10_Target_Location_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    UR10_Target_Location_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    UR10_Target_Location_socket.listen(1)
    UR10_Target_Location, address = UR10_Target_Location_socket.accept()  # accept new connection
    #print("Connection from: " + str(address))
    global POS_Y 

    global Target_Encoder
    while True:
        data = UR10_Target_Location.recv(1024).decode()
        # if data:
            
        # UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
        UR10_Target_Location.send(("POS_Y " + str(POS_Y) + "\n").encode())

        # UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
        #UR10_Target_Location.send(("Target_Encoder" + str(Target_Encoder) + "\n").encode())

        # receive data stream. it won't accept data packet greater than 1024 bytes
        
        print(str(data))
        # ur10.send(data.encode())  # send data to the client
        print(POS_Y)
# ###############################################################################
t1 = threading.Thread(target=get_encoder_count)
t1.start()
t2 = threading.Thread(target=send_target_location)
t2.start()
global Encoder_count
global POS_Y
skip = 0
# Main loop
while True:
    in_frame = queue.get()
    image = in_frame.getCvFrame()
    image = image[0:1080, 210:1725]
    gray_belt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_belt_blurred = cv2.GaussianBlur(gray_belt, (5, 5), 0)
    _, threshold = cv2.threshold(gray_belt_blurred, 110, 255, cv2.THRESH_BINARY)
    #_, threshold = cv2.threshold(gray_belt, 110, 255, cv2.THRESH_BINARY)
    # Detect the objects
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    object_detected = False
    valid_contour_count = 0
    required_contour_count = 5
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
        if area > 35100 :

            cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
            #cv2.rectangle((image, 20,20, (200,200), 5, (0, 0, 255), -1))
            cv2.polylines(image, [box], True, (255, 0, 0), 2)
            cv2.putText(image, "Width {:.2f} cm".format(object_width, 0), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "Height {:.2f} cm".format(object_height, 0), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "X {:.2f} CM".format(x/pixel_cm_ratio), (int(x - 40), int(y -35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(image, "Y {:.2f} CM".format(y/pixel_cm_ratio), (int(x - 40), int(y + 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
            
           
            
            
         
            
            
            # Encoder_count = 

            # Target_Encoder = Encoder_count + 332.5

        
            #print(Target_Encoder, Encoder_count)
            # first_time = True

            # # Bottom Left corner
            
            # # # Bottom Right corner 
            # cv2.circle(image, (1287, 895), 5, (0, 255, 0), -1)
            # # # Top Right corner 
            # cv2.circle(image, (1250, 198), 5, (0, 255, 0), -1)
            # # # Top Left corner
            # cv2.circle(image, (237 , 182), 5, (0, 255, 0), -1)
            # cv2.circle(image, (933, 701), 5, (0, 255, 0), -1)
       
        POS_Y_0 = +155.30
        X_ur10 = (x/pixel_cm_ratio)*10
        POS_Y = -1 * (X_ur10 + 135.30)
        #print(POS_Y)
    #cv2.circle(image, (1, 1), 5, (0, 255, 0), -1)
   
    start_time = time.time()
    cv2.imshow("Frame", image)
    #cv2.imshow("Cannyy", threshold)

    end_time = time.time()
    detection_time = end_time - start_time
    #print(detection_time)
    

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break



# import threading
# import cv2
# import depthai as dai
# import numpy as np
# import time
# import socket

# def initialize_pipeline():
#     pipeline = dai.Pipeline()

#     # Define camera nodes
#     color_cam = pipeline.createColorCamera()
#     color_cam.setPreviewSize(1920, 1080)
#     color_cam.setInterleaved(False)
#     color_cam.initialControl.setManualFocus(0)

#     # Set manual exposure and initial exposure time
#     exposure_time_us = 10000
#     iso_value = 600
#     color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

#     # Define output nodes
#     xout = pipeline.createXLinkOut()
#     xout.setStreamName("color")

#     # Link nodes
#     color_cam.preview.link(xout.input)

#     return pipeline

# def process_image(image):
#     gray_belt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray_belt_blurred = cv2.GaussianBlur(gray_belt, (5, 5), 0)
#     _, threshold = cv2.threshold(gray_belt_blurred, 110, 255, cv2.THRESH_BINARY)
#     contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     return contours

# def draw_contours(image, contours):
#     for cnt in contours:
#         # Calculate area & Perimeter
#         area = cv2.contourArea(cnt)
#         perimeter = cv2.arcLength(cnt, True)

#         # Calculate approximate polygonal curve
#         rect = cv2.minAreaRect(cnt)
#         (x, y), (w, h), angle = rect

#         # Display rectangle
#         box = cv2.boxPoints(rect)
#         box = np.intp(box)

#         pixel_cm_ratio = 10 / 0.8  # FHD
#         object_width = w / pixel_cm_ratio
#         object_height = h / pixel_cm_ratio

#         if area > 35100 and 0.5 < object_width / object_height < 2.0:
#             # Draw contour and polygon on the original image
#             cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
#             cv2.polylines(image, [box], True, (255, 0, 0), 2)
#             cv2.putText(image, "Width {:.2f} cm".format(object_width, 0), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Height {:.2f} cm".format(object_height, 0), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "X {:.2f} CM".format(x/pixel_cm_ratio), (int(x - 40), int(y -35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Y {:.2f} CM".format(y/pixel_cm_ratio), (int(x - 40), int(y + 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

#             X_ur10 = (x/pixel_cm_ratio)*10
#             POS_Y = -1 * (X_ur10 + 135.30)
#     return image

# def main_loop(queue):
#     global Encoder_count
#     global POS_Y

#     while True:
#         in_frame = queue.get()
#         image = in_frame.getCvFrame()
#         image = image[0:1080, 210:1725]

#         contours = process_image(image)
#         image = draw_contours(image, contours)

#         cv2.imshow("Frame", image)

#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             break

# def get_encoder_count():
#     # get the hostname
#     host = ""
#     port = 50001  # initiate port no above 1024

#     Encoder_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     Encoder_socket.bind((host, port))  # bind host address and port together
#     # configure how many client the server can listen simultaneously
#     Encoder_socket.listen(1)
#     UR10, address = Encoder_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))
#     global Encoder_count
#     while True: 
         
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         Encoder_count = UR10.recv(1024).decode()
#         #print(str(Encoder_count))
#         # ur10.send(data.encode())  # send data to the client

# def send_target_location():
#      # get the hostname
#     host = ""
#     port = 50000  # initiate port no above 1024

#     UR10_Target_Location_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     UR10_Target_Location_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     UR10_Target_Location_socket.listen(1)
#     UR10_Target_Location, address = UR10_Target_Location_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))
#     global POS_Y 

#     global Target_Encoder
#     while True:
#         data = UR10_Target_Location.recv(1024).decode()
#         # if data:
            
#         # UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
#         UR10_Target_Location.send(("POS_Y " + str(POS_Y) + "\n").encode())

#         # UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
#         #UR10_Target_Location.send(("Target_Encoder" + str(Target_Encoder) + "\n").encode())

#         # receive data stream. it won't accept data packet greater than 1024 bytes
        
#         print(str(data))
#         # ur10.send(data.encode())  # send data to the client
#         print(POS_Y)

# if __name__ == "__main__":
#     pipeline = initialize_pipeline()

#     # Create device and start pipeline
#     device = dai.Device(pipeline)
#     queue = device.getOutputQueue("color", maxSize=4, blocking=False)

#     t1 = threading.Thread(target=get_encoder_count)
#     t1.start()
#     t2 = threading.Thread(target=send_target_location)
#     t2.start()

#     main_loop(queue)

# import keyboard
# import time
# import socket

# def run_encoder_simulator():
#     # Define the resolution of the encoder (13333 ticks per meter)
#     TICKS_PER_METER = 13333

#     # Define the desired speed (0.25 meters per second)
#     SPEED = 0.25

#     # Initialize the encoder value to 0
#     encoder_value = 0

#     # Set up TCP socket for sending data
#     TCP_IP = "192.168.0.121"  # IP address of the destination device
#     TCP_PORT = 50001  # Port number for the destination application
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((TCP_IP, TCP_PORT))

#     # Define a function to update the encoder value based on key presses
#     def update_encoder():
#         nonlocal encoder_value
#         if keyboard.is_pressed('up'):
#             # Compute the change in encoder value based on the elapsed time and desired speed
#             dt = 1 # Use a fixed time interval of 1 second
#             ds = (SPEED * dt)/200
#             dencoder = ds * TICKS_PER_METER
#             encoder_value += int(dencoder)  # Convert to integer ticks

#         elif keyboard.is_pressed('down'):
#             # Compute the change in encoder value based on the elapsed time and desired speed
#             dt = 1  # Use a fixed time interval of 1 second
#             ds = (SPEED * dt)/200
#             dencoder = ds * TICKS_PER_METER
#             encoder_value -= int(dencoder)  # Convert to integer ticks

#     # Continuously update the encoder value based on key presses
#     while True:
#         update_encoder()

#         # Convert the encoder value to meters and send it over TCP
#         distance = encoder_value / TICKS_PER_METER
#         message = f"Encoder value: {encoder_value} ticks ({distance:.3f} meters)"
#         sock.sendall(message.encode(ascii))

#         time.sleep(0.01)

#     sock.close()

# run_encoder_simulator()
