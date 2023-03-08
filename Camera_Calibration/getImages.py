# import cv2

# cap = cv2.VideoCapture(2)

# num = 0

# while cap.isOpened():

#     succes, img = cap.read()

#     k = cv2.waitKey(5)

#     if k == 27:
#         break
#     elif k == ord('s'): # wait for 's' key to save and exit
#         cv2.imwrite('images/img' + str(num) + '.png', img)
#         print("image saved!")
#         num += 1

#     cv2.imshow('Img',img)

# # Release and destroy all windows before termination
# cap.release()

# cv2.destroyAllWindows()
# #





# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2028)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1520)

# num = 0

# while cap.isOpened():

#     success, img = cap.read()

#     k = cv2.waitKey(5)

#     if k == 27:
#         break
#     elif k == ord('s'): # wait for 's' key to save and exit
#         cv2.imwrite('img' + str(num) + '.png', img)
#         print("image saved!")
#         num += 1

#     cv2.imshow('Img',img)

# # Release and destroy all windows before termination
# cap.release()
# cv2.destroyAllWindows()




import time
import picamera

# Create a new PiCamera object
camera = picamera.PiCamera()

# Set the resolution of the camera
camera.resolution = (1024, 768)

# Set the preview window size
camera.start_preview(fullscreen=False, window=(0, 0, 1024, 768))



# Capture multiple images
for i in range(1, 15):
    # Wait for the preview to initialize
    time.sleep(10)
    # Capture an image and save it to a file
    camera.capture(f'img{i}.jpg')
    print('done',i ) 
# Stop the preview
camera.stop_preview()
