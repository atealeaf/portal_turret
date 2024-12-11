# # Run `export QT_QPA_PLATFORM=offscreen` in terminal for it to work!!

from picamera2 import Picamera2
import time
import numpy as np
import cv2

# Initialize the Picamera2 instance
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# Start the camera
picam2.start()
time.sleep(0.1)  # Allow the camera to warm up

# Initialize the HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    # Capture a frame as a NumPy array
    image = picam2.capture_array()

    # Ensure image is in BGR format
    if image.shape[2] == 4:  # If the image has an alpha channel (BGRA)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    elif len(image.shape) == 2:  # If grayscale, convert to BGR for consistency
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Convert to grayscale for HOG detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
    # Draw detected boxes
    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        print("human detected")
    
    
    # Display the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    # Break on 'q' key press
    if key == ord("q"):
        break

# Stop the camera and close OpenCV windows
picam2.stop()
cv2.destroyAllWindows()

# import argparse
# import sys
# import time

# import numpy as np

# from picamera2 import CompletedRequest, MappedArray, Picamera2
# from picamera2.devices.imx500 import IMX500, NetworkIntrinsics
# from picamera2.devices.imx500.postprocess import COCODrawer
# from picamera2.devices.imx500.postprocess_highernet import \
#     postprocess_higherhrnet

# last_boxes = None
# last_scores = None
# last_keypoints = None
# WINDOW_SIZE_H_W = (480, 640)


# def ai_output_tensor_parse(metadata: dict):
#     """Parse the output tensor into a number of detected objects, scaled to the ISP output."""
#     global last_boxes, last_scores, last_keypoints
#     np_outputs = imx500.get_outputs(metadata=metadata, add_batch=True)
#     if np_outputs is not None:
#         keypoints, scores, boxes = postprocess_higherhrnet(outputs=np_outputs,
#                                                            img_size=WINDOW_SIZE_H_W,
#                                                            img_w_pad=(0, 0),
#                                                            img_h_pad=(0, 0),
#                                                            detection_threshold=args.detection_threshold,
#                                                            network_postprocess=True)

#         if scores is not None and len(scores) > 0:
#             last_keypoints = np.reshape(np.stack(keypoints, axis=0), (len(scores), 17, 3))
#             last_boxes = [np.array(b) for b in boxes]
#             last_scores = np.array(scores)
#     return last_boxes, last_scores, last_keypoints


# def ai_output_tensor_draw(request: CompletedRequest, boxes, scores, keypoints, stream='main'):
#     """Draw the detections for this request onto the ISP output."""
#     with MappedArray(request, stream) as m:
#         if boxes is not None and len(boxes) > 0:
#             drawer.annotate_image(m.array, boxes, scores,
#                                   np.zeros(scores.shape), keypoints, args.detection_threshold,
#                                   args.detection_threshold, request.get_metadata(), picam2, stream)


# def picamera2_pre_callback(request: CompletedRequest):
#     """Analyse the detected objects in the output tensor and draw them on the main output image."""
#     boxes, scores, keypoints = ai_output_tensor_parse(request.get_metadata())
#     ai_output_tensor_draw(request, boxes, scores, keypoints)


# def get_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model", type=str, help="Path of the model",
#                         default="/usr/share/imx500-models/imx500_network_higherhrnet_coco.rpk")
#     parser.add_argument("--fps", type=int, help="Frames per second")
#     parser.add_argument("--detection-threshold", type=float, default=0.3,
#                         help="Post-process detection threshold")
#     parser.add_argument("--labels", type=str,
#                         help="Path to the labels file")
#     parser.add_argument("--print-intrinsics", action="store_true",
#                         help="Print JSON network_intrinsics then exit")
#     return parser.parse_args()


# def get_drawer():
#     categories = intrinsics.labels
#     categories = [c for c in categories if c and c != "-"]
#     return COCODrawer(categories, imx500, needs_rescale_coords=False)


# if __name__ == "__main__":
#     args = get_args()

#     # This must be called before instantiation of Picamera2
#     imx500 = IMX500(args.model)
#     intrinsics = imx500.network_intrinsics
#     if not intrinsics:
#         intrinsics = NetworkIntrinsics()
#         intrinsics.task = "pose estimation"
#     elif intrinsics.task != "pose estimation":
#         print("Network is not a pose estimation task", file=sys.stderr)
#         exit()

#     # Override intrinsics from args
#     for key, value in vars(args).items():
#         if key == 'labels' and value is not None:
#             with open(value, 'r') as f:
#                 intrinsics.labels = f.read().splitlines()
#         elif hasattr(intrinsics, key) and value is not None:
#             setattr(intrinsics, key, value)

#     # Defaults
#     if intrinsics.inference_rate is None:
#         intrinsics.inference_rate = 10
#     if intrinsics.labels is None:
#         with open("assets/coco_labels.txt", "r") as f:
#             intrinsics.labels = f.read().splitlines()
#     intrinsics.update_with_defaults()

#     if args.print_intrinsics:
#         print(intrinsics)
#         exit()

#     drawer = get_drawer()

#     picam2 = Picamera2(imx500.camera_num)
#     config = picam2.create_preview_configuration(controls={'FrameRate': intrinsics.inference_rate}, buffer_count=12)

#     imx500.show_network_fw_progress_bar()
#     picam2.start(config, show_preview=True)
#     imx500.set_auto_aspect_ratio()
#     picam2.pre_callback = picamera2_pre_callback

#     while True:
#         time.sleep(0.5)
# from picamera2 import Picamera2
# import cv2
# import time
# import numpy as np


# picam2 = Picamera2()
# picam2.configure(picam2.create_video_configuration(main={"format": 'RGB888', "size": (640, 480)}))
# picam2.start()

# print("Recording... Press Ctrl+C to stop.")
# prev = None
# start_time = time.time()
# while time.time() - start_time < 100:  # Record for 10 seconds
#     frame = picam2.capture_array()
#     # Display the video feed in a window
#     cv2.imshow('Camera Feed', frame)
#     if prev is not None:
#         mse = np.square(np.subtract(frame, prev)).mean()
#         if mse > 7:
#             print("Movement!")
           
           
           
#         else:
#             print("All good")

       
       
#     # Press 'q' to exit early
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         picam2.close()
#         cv2.destroyAllWindows()  # Close the window
#         print("Recording stopped.")
   
#     prev = frame
#export QT_QPA_PLATFORM=xcb



