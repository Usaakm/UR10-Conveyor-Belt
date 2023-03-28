import cv2
import depthai as dai
import numpy as np
import time
import cv2.cuda as cuda

# Create pipeline
pipeline = dai.Pipeline()

# Define camera nodes
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Create XLink output for video frames
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

# Create DepthAI device and start pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the rgb frames from the output defined above
    q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    # Create window for display
    cv2.namedWindow("DepthAI Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("DepthAI Camera", 640, 480)

    # Main loop
    while True:
        # Get the latest rgb frame
        in_rgb = q_rgb.get()
        frame_rgb = in_rgb.getCvFrame()

        # Upload rgb frame to GPU
        frame_rgb_gpu = cuda.GpuMat()
        frame_rgb_gpu.upload(frame_rgb)

        # Convert rgb frame to grayscale
        frame_gray_gpu = cuda.cvtColor(frame_rgb_gpu, cv2.COLOR_BGR2GRAY)

        # Download grayscale frame from GPU
        frame_gray_gpu = cv2.cuda.resize(frame_gray_gpu, (640, 480))
        frame_gray = frame_gray_gpu.download()

        # Remove third dimension from rgb frame
        frame_rgb = np.squeeze(frame_rgb)

        # Add third dimension to grayscale frame
        frame_gray = np.expand_dims(frame_gray, axis=2)

        # Display rgb frame and grayscale frame side-by-side
        frame_concat = np.concatenate((frame_rgb, frame_gray), axis=1)
        cv2.imshow("DepthAI Camera", frame_concat)

        # Check for key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()
