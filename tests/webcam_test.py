import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0) # Initialize the webcam
detector = PoseDetector() # Initialize the pose detector

while True:

    success, img = cap.read() # Read a frame from the webcam
    # Detect poses
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)

    # If poses are detected, print the position of the first landmark
    if lmList:
        print(lmList[0])

    # Display the image
    cv2.imshow("Image", img)

    # Break the loop if ‘q’ is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
    success, img = cap.read() # Read a frame from the webcam