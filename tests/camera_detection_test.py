import cv2
from picamera2 import Picamera2

# Initialize OpenCV window
cv2.startWindowThread()

# Initialize Picamera2 and configure the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

while True:
    # Capture frame-by-frame
    im = picam2.capture_array()

    # Display the resulting frame
    cv2.imshow("Camera", im)
   
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cv2.destroyAllWindows()


# from picamera2 import Picamera2, Preview
# import time

# picam2 = Picamera2()

# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)

# picam2.start_preview(Preview.QT)
# picam2.start()

# time.sleep(2)

# picam2.capture_file("test_photo.jpg")