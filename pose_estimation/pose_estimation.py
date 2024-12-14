import cv2
import mediapipe as mp
import numpy as np
import functions
from collections import deque
import time

import matplotlib.pyplot as plt

# Initialize timer
last_wave_detection_time = time.time()


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

FRAME_RATE = 30  # Frames per second
seconds = 3
WINDOW_SIZE = FRAME_RATE * seconds

# Deques to store the last 3 seconds of angles
left_angle_list = deque(maxlen=WINDOW_SIZE)
right_angle_list = deque(maxlen=WINDOW_SIZE)

cap = cv2.VideoCapture(0)


while cap.isOpened():
   # Read frame
   _, frame = cap.read()

   # Convert frame to RGB
   frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

   # Process the frame for pose detection
   pose_results = pose.process(frame_rgb)

   if pose_results.pose_landmarks:
       # Extract keypoints
       left_shoulder = pose_results.pose_landmarks.landmark[11]
       left_elbow = pose_results.pose_landmarks.landmark[13]
       left_wrist = pose_results.pose_landmarks.landmark[15]
       right_shoulder = pose_results.pose_landmarks.landmark[12]
       right_elbow = pose_results.pose_landmarks.landmark[14]
       right_wrist = pose_results.pose_landmarks.landmark[16]
       head = pose_results.pose_landmarks.landmark[0]
    #    print(left_wrist)
       # Calculate angles
       left_angle = functions.calculate_angle(left_shoulder, left_elbow, left_wrist)
       right_angle = functions.calculate_angle(right_shoulder, right_elbow, right_wrist)

       # Append angles
       left_angle_list.append(left_angle)
       right_angle_list.append(right_angle)

       # Check if 3 seconds have passed since the last wave detection
       current_time = time.time()
       if current_time - last_wave_detection_time >= 3:  

           left_wave_detected = functions.detect_wave_motion(list(left_angle_list), left_wrist, left_elbow)
           right_wave_detected = functions.detect_wave_motion(list(right_angle_list), right_wrist, right_elbow)
           
           # Print results
           print(f"Left Wave Detected: {left_wave_detected}")
           print(f"Right Wave Detected: {right_wave_detected}")
         #   print(left_angle_list)
        #    print(right_angle_list)
           # Update the timer
        #    print(left_angle_list)
           last_wave_detection_time = current_time
           functions.follow_human(head)
    
      
       # Draw skeleton on the frame
       mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

       # Display the left angle on the frame
       left_shoulder_coords = tuple(np.multiply([left_shoulder.x, left_shoulder.y], [640, 480]).astype(int))
       cv2.putText(frame, f"{int(left_angle)}°", left_shoulder_coords, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

   # Display the frame
   cv2.imshow('Output', frame)

   # Exit loop on 'q' key press
   if cv2.waitKey(1) == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()

