import cv2
import mediapipe as mp
import time

class PoseDetector():
    def __init__(self, staticImageMode=False, modelComplexity=1, smoothLandmarks=True, enableSegmentation=False, smoothSegmentation=True, minDetectionConfidence=0.5, minTrackingConfidence=0.5):
        self.staticImageMode = staticImageMode
        self.modelComplexity = modelComplexity
        self.smoothLandmarks = smoothLandmarks
        self.enableSegmentation = enableSegmentation
        self.smoothSegmentation = smoothSegmentation
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.staticImageMode, self.modelComplexity, self.smoothLandmarks, self.enableSegmentation, self.smoothSegmentation, self.minDetectionConfidence, self.minTrackingConfidence)
    
    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img
    
    def findPosition(self, img, draw=False):
        lmList = []
        for id, lm in enumerate(self.results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)

            lmList.append([id, cx, cy])

            if draw:
                cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return lmList

    

def main():
    # Use the default camera (index 0). Change the index if you have multiple cameras.
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    detector = PoseDetector()
    pTime = 0

    while True:
        success, img = cap.read()

        # Check if the frame was successfully captured
        if not success or img is None:
            print("Failed to capture frame from camera.")
            break

        # Process the frame for pose detection
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        # Print landmarks if detected
        if len(lmList) != 0:
            print(lmList)

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        # Display the frame
        # cv2.imshow("Real-Time Pose Detection", img)
        cv2.imwrite("frame.jpg", img)

        # Exit loop if 'q' is pressed or window is closed
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Real-Time Pose Detection", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()