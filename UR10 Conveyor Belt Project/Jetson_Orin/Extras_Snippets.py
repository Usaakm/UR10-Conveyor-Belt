# import cv2
# import depthai as dai
# import numpy as np
# import time 
# import socket


# # Create pipeline
# pipeline = dai.Pipeline()

# # Define camera nodes
# color_cam = pipeline.createColorCamera()
# #color_cam.setPreviewSize(1280, 720)
# color_cam.setPreviewSize(1920, 1080)


# color_cam.setInterleaved(False)
# color_cam.initialControl.setManualFocus(0)

# # Set manual exposure and initial exposure time
# exposure_time_us = 10000
# iso_value = 500
# color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

# # Define output nodes
# xout = pipeline.createXLinkOut()
# xout.setStreamName("color")

# # Link nodes
# color_cam.preview.link(xout.input)

# # Create device and start pipeline
# device = dai.Device(pipeline)
# queue = device.getOutputQueue("color", maxSize=4, blocking=False)


# def get_encoder_count():
#     # get the hostname
#     host = "192.168.0.2"
#     port = 50001  # initiate port no above 1024

#     Encoder_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     Encoder_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     Encoder_socket.listen(1)
#     UR10, address = Encoder_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))

#     # receive data stream. it won't accept data packet greater than 1024 bytes
#     Ecoder_count = UR10.recv(1024).decode()
#     print(str(Ecoder_count))
#     # ur10.send(data.encode())  # send data to the client

# ##############################################################################
# def send_target_location():
#     # get the hostname
#     host = ""
#     port = 50000  # initiate port no above 1024

#     UR10_Target_Location_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     UR10_Target_Location_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     UR10_Target_Location_socket.listen(1)
#     UR10_Target_Location, address = UR10_Target_Location_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))
#     POS_X = 1500
#     POS_Y = 2500

#     UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
#     UR10_Target_Location.send(("POS_Y " + str(POS_X) + "\n").encode())

#     # receive data stream. it won't accept data packet greater than 1024 bytes
#     data = UR10_Target_Location.recv(1024).decode()
#     print(str(data))
#     # ur10.send(data.encode())  # send data to the client
# ###############################################################################


# do = True

# # Main loop
# while True:
#     in_frame = queue.get()
#     image = in_frame.getCvFrame()
#     image = image[0:1080, 200:1725]
#     gray_belt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, threshold = cv2.threshold(gray_belt, 150, 255, cv2.THRESH_BINARY)

#     # Detect the objects
#     contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

#         #pixel_cm_ratio = 10 / 1.2 # HD
#         pixel_cm_ratio = 10 / 0.8 # FHD

#         # Get Width and Height of the Objects by applying the Ratio pixel to cm
#         object_width = w / pixel_cm_ratio
#         object_height = h / pixel_cm_ratio

#         # Draw contour and polygon on original image
#         if area > 5000:
#             cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
#             #print(int(x), int(y))
#             #cv2.rectangle((image, 20,20, (200,200), 5, (0, 0, 255), -1))
#             cv2.polylines(image, [box], True, (255, 0, 0), 2)
#             cv2.putText(image, "Width {:.2f} cm".format(object_width, 0), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Height {:.2f} cm".format(object_height, 0), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "X {:.2f} CM".format(x/pixel_cm_ratio), (int(x - 40), int(y -35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Y {:.2f} CM".format(y/pixel_cm_ratio), (int(x - 40), int(y + 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             # new = -0.135 - (x/10)
#             # new = new/100

#             # while do :
#             #     s.send("movej(p[0.4, -0.999, 0.03, 3.1, 0, 0], a=0.5, v=0.25)\n".encode())
#             #     print(new)
#             #     do= False


#         cv2.imshow("Frame", image)

#         #cv2.circle(image, (1, 1), 5, (0, 255, 0), -1)
#         # start_time = time.time()
#         # end_time = time.time()
#         # detection_time = end_time - start_time
#         #print(detection_time)
    

#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break


































# import threading
# import cv2
# import depthai as dai
# import numpy as np
# import time 
# import socket
# import queue

# # Create pipeline
# pipeline = dai.Pipeline()

# # Define camera nodes
# color_cam = pipeline.createColorCamera()
# #color_cam.setPreviewSize(1280, 720)
# color_cam.setPreviewSize(1920, 1080)


# color_cam.setInterleaved(False)
# color_cam.initialControl.setManualFocus(0)

# # Set manual exposure and initial exposure time
# exposure_time_us = 10000
# iso_value = 600
# color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

# # Define output nodes
# xout = pipeline.createXLinkOut()
# xout.setStreamName("color")

# # Link nodes
# color_cam.preview.link(xout.input)

# # Create device and start pipeline
# device = dai.Device(pipeline)
# img_queue = device.getOutputQueue("color", maxSize=4, blocking=False)








# encoder_count_queue = queue.Queue()

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
#         encoder_count_queue.put(Encoder_count)

#         print(str(Encoder_count))
#         # ur10.send(data.encode())  # send data to the client

# # # ###############################################################################







# def send_target_location():
#     # get the hostname
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
# # ###############################################################################





# t1 = threading.Thread(target=get_encoder_count)
# t1.start()
# t2 = threading.Thread(target=send_target_location)
# t2.start()




# global Encoder_count
# global POS_Y
# skip = 0
# # Main loop
# while True:
#     in_frame = img_queue.get()
#     image = in_frame.getCvFrame()
#     image = image[0:1080, 210:1725]
#     gray_belt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray_belt_blurred = cv2.GaussianBlur(gray_belt, (5, 5), 0)
#     _, threshold = cv2.threshold(gray_belt_blurred, 110, 255, cv2.THRESH_BINARY)
#     #_, threshold = cv2.threshold(gray_belt, 110, 255, cv2.THRESH_BINARY)
#     # Detect the objects
#     contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     object_detected = False
#     valid_contour_count = 0
#     required_contour_count = 5
    
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

#         #pixel_cm_ratio = 10 / 1.2 # HD
#         pixel_cm_ratio = 10 / 0.8 # FHD
#         # Get Width and Height of the Objects by applying the Ratio pixel to cm
#         object_width = w / pixel_cm_ratio
#         object_height = h / pixel_cm_ratio
        
      

#         # Draw contour and polygon on original image
#         if area > 90000 and area < 110000:
#             cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
#             #cv2.rectangle((image, 20,20, (200,200), 5, (0, 0, 255), -1))
#             cv2.polylines(image, [box], True, (255, 0, 0), 2)
#             cv2.putText(image, "Width {:.2f} cm".format(object_width, 0), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Height {:.2f} cm".format(object_height, 0), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "X {:.2f} CM".format(x/pixel_cm_ratio), (int(x - 40), int(y -35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Y {:.2f} CM".format(y/pixel_cm_ratio), (int(x - 40), int(y + 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
            
           
            
            
        
            
            
            

#             #Target_Encoder = Encoder_count + 13333

        
#             #print(Target_Encoder, Encoder_count)
#             # first_time = True

#             POS_Y_0 = +155.30
#             X_ur10 = (x/pixel_cm_ratio)*10
#             POS_Y = -1 * (X_ur10 + 135.30)
#             #print(POS_Y)
   
#     cv2.imshow("Frame", image)
    

#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break


##################################################################################################################################################

# def send_target_location(POS_Y, x_ur10):
#     # get the hostname
#     host = ""
#     port = 50000  # initiate port no above 1024

#     UR10_Target_Location_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     UR10_Target_Location_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     UR10_Target_Location_socket.listen(1)
#     UR10_Target_Location, address = UR10_Target_Location_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))

#     global Target_Encoder
   
#     Target_Encoder = 0

#     while True:
     
        
#                 # host = ""
#                 # port = 30002  # initiate port no above 1024

#                 # UR10_Target_Location_socket = socket.socket()  # get instance
#                 # # look closely. The bind() function takes tuple as argument
#                 # UR10_Target_Location_socket.bind((host, port))  # bind host address and port together

#                 # # configure how many client the server can listen simultaneously
#                 # UR10_Target_Location_socket.listen(1)
#                 # UR10_Target_Location, address = UR10_Target_Location_socket.accept()  # accept new connection

#                 # UR10_Target_Location.send((str(True)).encode())


#         #Get Encoder_count from queue
#         if not encoder_count_queue.empty():
#             Encoder_count = encoder_count_queue.get()
#             Target_Encoder = Encoder_count + 17472


#         POS_Y_0 = 135.30
#         X_ur10 = (x_ur10/pixel_cm_ratio)*10
#         POS_Y = -1 * (X_ur10 + POS_Y_0)
#         print(POS_Y)
#         # UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
#         UR10_Target_Location.send(("POS_Y " + str(POS_Y) + "\n").encode())

#         #UR10_Target_Location.send(("POS_X " + str(POS_X) + "\n").encode())
   
    
#     Bool_UR10.send((str(True)).encode())

#     #time.sleep(0.3)
  



import socket
import queue
import threading

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
        # receive data stream. it won't accept data packet greater than 1024 bytes
        Encoder_count = UR10.recv(1024).decode()
        #print(Encoder_count)
        encoder_count_queue.put(Encoder_count)

def send_target_location(encoder_count_queue):
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

    while True:    
        encoder_count_str = encoder_count_queue.get()#.strip()  # Remove any whitespace or newline characters
        encoder_count = float(encoder_count_str)  # Convert the string to a float, then to an integer
        print("Encoder count:", encoder_count)
        Target_Encoder = encoder_count + 17472
        print("Target Encoder:", Target_Encoder)

        data = UR10_Target_Location.recv(1024).decode()
        print("Data received:", data)

        UR10_Target_Location.send(("Target_Encoder" + str(Target_Encoder) + "\n").encode())




encoder_count_queue = queue.Queue()
t1 = threading.Thread(target=get_encoder_count, args=(encoder_count_queue,))
t1.start()

t2 = threading.Thread(target=send_target_location, args=(encoder_count_queue,))
t2.start()
