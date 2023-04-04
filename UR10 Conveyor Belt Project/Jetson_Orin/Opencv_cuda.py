
# import cv2

# # Check if CUDA support is available
# if cv2.cuda.getCudaEnabledDeviceCount() > 0:
#     print("CUDA is supported")
# else:
#     print("CUDA is not supported")






# import cv2
# import depthai as dai
# import numpy as np
# import time 
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
# iso_value = 400
# color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

# # Define output nodes
# xout = pipeline.createXLinkOut()
# xout.setStreamName("color")

# # Link nodes
# color_cam.preview.link(xout.input)

# # Create device and start pipeline
# device = dai.Device(pipeline)
# queue = device.getOutputQueue("color", maxSize=4, blocking=False)

# # Main loop
# while True:
#     in_frame = queue.get()
#     image = in_frame.getCvFrame()
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
#         box = np.int0(box)

#         pixel_cm_ratio = 10 / 1.2
#         # Get Width and Height of the Objects by applying the Ratio pixel to cm
#         object_width = w / pixel_cm_ratio
#         object_height = h / pixel_cm_ratio

#         # Draw contour and polygon on original image
#         if area > 5000:
#             cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
#             cv2.polylines(image, [box], True, (255, 0, 0), 2)
#             cv2.putText(image, "Width {} cm".format(round(object_width, 0)), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Height {} cm".format(round(object_height, 0)), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        
#         start_time = time.time()
#         cv2.imshow("Frame", image)
#         end_time = time.time()
#         detection_time = end_time - start_time
#         print(detection_time)
       
    
#     # # Change exposure time with 'u' (increase) and 'd' (decrease) keys
#     key = cv2.waitKey(1) & 0xFF
#     # if key == ord('u'):
#     #     exposure_time_us += 1000
#     #     color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)
#     # elif key == ord('d'):
#     #     exposure_time_us -= 1000
#     #     color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)
#     # # Exit loop when 'q' is pressed
#     if key == ord('q'):
#         break

# # Close OpenCV windows




# import cv2
# import depthai as dai
# import numpy as np
# import time
# import cv2.cuda as cuda
# # Create pipeline
# pipeline = dai.Pipeline()

# # Define camera nodes
# color_cam = pipeline.createColorCamera()
# color_cam.setPreviewSize(1920, 1080)
# color_cam.setInterleaved(False)
# color_cam.initialControl.setManualFocus(0)

# # Set manual exposure and initial exposure time
# exposure_time_us = 10000
# iso_value = 400
# color_cam.initialControl.setManualExposure(exposure_time_us, iso_value)

# # Define output nodes
# xout = pipeline.createXLinkOut()
# xout.setStreamName("color")

# # Link nodes
# color_cam.preview.link(xout.input)

# # Create device and start pipeline
# device = dai.Device(pipeline)
# queue = device.getOutputQueue("color", maxSize=4, blocking=False)

# # Main loop
# while True:
#     in_frame = queue.get()
#     image = in_frame.getCvFrame()
#     image_gpu = cv2.cuda.GpuMat()
#     image_gpu.upload(image)

#     gray_belt_gpu = cuda.cvtColor(image_gpu, cv2.COLOR_BGR2GRAY)
#     height, width = gray_belt_gpu.size()
#     gray_belt = cv2.cuda.createContinuous(height, width, gray_belt_gpu.type())

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
#         box = np.int0(box)

#         pixel_cm_ratio = 10 / 1.2
#         # Get Width and Height of the Objects by applying the Ratio pixel to cm
#         object_width = w / pixel_cm_ratio
#         object_height = h / pixel_cm_ratio

#         # Draw contour and polygon on original image
#         if area > 5000:
#             cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
#             cv2.polylines(image, [box], True, (255, 0, 0), 2)
#             cv2.putText(image, "Width {} cm".format(round(object_width, 0)), (int(x - 40), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#             cv2.putText(image, "Height {} cm".format(round(object_height, 0)), (int(x - 40), int(y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

#         start_time = time.time()
#         cv2.imshow("Frame", image)
#         end_time = time.time()
#         detection_time = end_time - start_time

#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break

# # Close OpenCV windows
# cv2.destroyAllWindows()








