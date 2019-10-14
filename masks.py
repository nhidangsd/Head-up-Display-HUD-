import cv2
import numpy as np
import colors as color


"""
This function below will prepare and return the mask to overlay
Input:  
    # frame: the video frame's name

Output:
    # dilated_blue_mask
"""


def get_blue_mask(frame):

    # blur the frame to remove noises
    blur_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)

    # Prepare the mask to overlay
    blue_mask = cv2.inRange(hsv_frame, color.lower_blue, color.upper_blue)

    # Init kernel for erosion and dilation usage:
    kernel = np.ones((5, 5), np.uint8)
    # Erosion removes white noises, but it also shrinks object
    # So we dilate the object to increase the it as the noise is gone after the erosion
    eroded_blue_mask = cv2.erode(blue_mask, kernel, iterations=1)
    dilated_blue_mask = cv2.dilate(eroded_blue_mask, kernel, iterations=1)

    return dilated_blue_mask

