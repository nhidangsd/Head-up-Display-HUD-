import cv2


"""
This function below will draw the Head up display(HUD) on the frame
Input:  
    # frame: the video frame's name
    # color: any RBG color(can use any pre-defined color in colors.py)
    # center_x: the coordinate x of camera's Center
    # center_y: the coordinate y of camera's Center
    # center_radius: the the radius range from camera's center
    
Output:
    # No output
"""


def create_hud(frame, color, center_x, center_y, center_radius):
    # draw 4 corners:
    cv2.line(frame, (10, 10), (60, 10), color, 2)
    cv2.line(frame, (10, 10), (10, 60), color, 2)

    cv2.line(frame, (1270, 10), (1220, 10), color, 2)
    cv2.line(frame, (1270, 10), (1270, 60), color, 2)

    cv2.line(frame, (10, 710), (60, 710), color, 2)
    cv2.line(frame, (10, 710), (10, 660), color, 2)

    cv2.line(frame, (1270, 710), (1220, 710), color, 2)
    cv2.line(frame, (1270, 710), (1270, 660), color, 2)

    # draw left curve
    cv2.line(frame, (70, 100), (70, 620), color, 3)
    cv2.line(frame, (70, 100), (110, 80), color, 3)
    cv2.line(frame, (70, 620), (110, 640), color, 3)

    # draw right curve
    cv2.line(frame, (1210, 100), (1210, 620), color, 3)
    cv2.line(frame, (1170, 80), (1210, 100), color, 3)
    cv2.line(frame, (1170, 640), (1210, 620), color, 3)

    # draw center circle
    cv2.circle(frame, (center_x, center_y), center_radius, color, 1)
    cv2.circle(frame, (center_x, center_y), center_radius - 5, color, 2)
    cv2.circle(frame, (center_x, center_y), 1, color, 2)

    # draw target lines inside center circle
    cv2.line(frame, (center_x + 12, center_y), (center_x + 45, center_y), color, 1)
    cv2.line(frame, (center_x - 12, center_y), (center_x - 45, center_y), color, 1)
    cv2.line(frame, (center_x, center_y + 12), (center_x, center_y + 45), color, 1)
    cv2.line(frame, (center_x, center_y - 12), (center_x, center_y - 45), color, 1)


"""
This function below will return the current position of the target comparing to the camera center radius
Input:  
    # target_pos_x: the coordinate x of target's Center
    # target_pos_y: the coordinate y of target's Center
    # center_x: the coordinate x of camera's Center
    # center_y: the coordinate y of camera's Center
    # center_radius: the the radius range from camera's center
    
Output:
    # position: a string informing target's position
"""


def get_target_position(target_pos_x, target_pos_y, center_x, center_y, center_radius):

    # If target on left side of the camera
    if target_pos_x <= (center_x - center_radius):

        # Target is at upper left camera
        if target_pos_y <= (center_y - center_radius):
            position = 'UPPER LEFT Camera'
        # Target is at lower left camera
        elif target_pos_y >= (center_y + center_radius):
            position = 'LOWER LEFT Camera'
        # Target is at left side camera
        else:
            position = 'LEFT Camera'

    # Similarly, check coordinate target_y when target on the right side of the camera
    elif target_pos_x >= (center_x + center_radius):

        if target_pos_y <= (center_y - center_radius):
            position = 'UPPER RIGHT Camera'
        elif target_pos_y >= (center_y + center_radius):
            position = 'LOWER RIGHT Camera'
        else:
            position = 'RIGHT Camera'

    # else If target is above camera
    elif target_pos_y < (center_y - center_radius):
        position = 'ABOVE Camera'
    # else Target is below camera
    else:
        position = 'BELOW Camera'

    return position





