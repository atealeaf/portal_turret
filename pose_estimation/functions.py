import math
import numpy as np
from scipy.signal import argrelextrema
import numpy as np
from scipy.signal import find_peaks
from scipy.fftpack import fft
# from time import


def calculate_angle(joint1, joint2, joint3):
   """
   Calculate the angle between three joints.

   Returns the angle.
   """
   
   vector1 = [joint1.x - joint2.x, joint1.y - joint2.y]
   vector2 = [joint3.x - joint2.x, joint3.y - joint2.y]
   
   dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
   magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
   magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)
   
   if magnitude1 == 0 or magnitude2 == 0:
       return None
   
   angle = math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))
   return angle





# def detect_wave_motion(angle_deque, wrist, elbow):
#     """
#     Function to detect wave motion based on wrist movement.
#     angle_list: a list of angles in the last 3 seconds of any given live stream with 30fps.
   
#     Returns:
#        True if wave detected, False otherwise.
#     """

#     wave_detected = False
#     angle_list = list(angle_deque)

#     if wrist.y > elbow.y:
      
#         max_difference = max(angle_list) - min(angle_list)
#         inflection_count = 0
#         if max_difference > 10:
         
#             for i in range(len(angle_list) - 2):  
#                     prev_angle = angle_list[i]
#                     current_angle = angle_list[i+1]
#                     next_angle = angle_list[i + 2]
                    
#                     # Check for peaks or valleys with a threshold
#                     if (current_angle > (prev_angle + 3) and current_angle > (next_angle + 3)) or \
#                         (current_angle < (prev_angle - 3) and current_angle < (next_angle - 3)):
#                         inflection_count += 1
#                         print(inflection_count)
                    
#                 # Check if the number of inflection points exceeds the threshold for a wave.
#                     if inflection_count >= 3:  # Threshold for wave detection
#                       wave_detected = True

#     return wave_detected



def detect_wave_motion(angle_deque, wrist, elbow):
    """
    Function to detect wave motion based on wrist movement.
    angle_deque: A deque or list of angles.

    Returns:
        True if at least 3 waves are detected, False otherwise.
    """
    wave_detected = False
    print(wrist.y>elbow.y)
    if wrist.y <elbow.y:
        
        angle_list = list(angle_deque)
        
        if max(angle_list)-min(angle_list) > 10:
            wave_count = 0
            increasing = []

            for i in range(1, len(angle_list)):
                if angle_list[i] > (angle_list[i - 1]):
                    increasing.append(1)
                    # print("1")
                else:
                    increasing.append(0)
                    # print("0")
                # print(increasing)
            for j in range(1, (len(increasing)-1)): 
                if increasing[j]  !=  increasing[j+1]:
                    wave_count += 1
                # print(wave_count)
                # Break early if 3 waves are detected
            if wave_count >= 3:
                wave_detected = True
            

    return wave_detected



def follow_human(head_pose, num_LED):
   """
   section vision window into sections based on how many LEDs there are. Categorize where the head pose is
   and light up LED based on position to simulate eye tracking.
   we are imagining the leds are installed in a n by n square. 
   so the actual numbers of led would equal to num_LED*num_LED where num_LED = n
   returns the index of where the head is in the grid world
   Ex. if the head is in the middel grid of a 3 by 3 grid it sould return
   [1, 1] as the count starts from 0.
   """
   section_len = 1/num_LED
   x_index = math.floor(head_pose.x /section_len )
   y_index= math.floor(head_pose.y/section_len)

   return [x_index, y_index]

def detect_gesture(arm_angle, torso_arm_angle):
    """
    detects the gesture of holding arm out to either left or right to activate wing
    movement in the turret.

    Returns true or false
    """
    if 170 < arm_angle < 190:
        if  80 <torso_arm_angle< 100:
            return True
    

