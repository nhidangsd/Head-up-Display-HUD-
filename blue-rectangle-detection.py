import cv2
import numpy as np
import colors as color
import masks
import HUD

# Open camera number 0
cap = cv2.VideoCapture(0)

# Find coordinates X and Y of the Frame's center
cap_center_x = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
cap_center_y = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
# Set camera center radius to 80 for HUD usage
cap_center_radius: int = 80

while cap.isOpened():

    # Default HUD when there is no Target in the frame:
    #   Color: White
    #   Target: 'NONE'
    hud_color = color.white
    hud_info = 'NONE'

    # load the frame
    _, frame = cap.read()

    # Find all contours and save them in array contours :
    contours, _ = cv2.findContours(masks.get_blue_mask(frame), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        # get the area of the contour using contourARea
        area = cv2.contourArea(cnt)

        # To eliminate noises that also have blue color in the frame
        # Only show contour if target area is greater than 2600
        if area > 2600:

            # epsilon- is maximum distance from contour to approximated contour - set as 1% in our case
            # epsilon = error_rate * actual_arc_length
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            # Use epsilon to approximate a rectangle
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # compute the center of the contour
            M = cv2.moments(approx)
            cnt_center_x = int(M['m10'] / M['m00'])
            cnt_center_y = int(M['m01'] / M['m00'])

            # If Target exist in the frame
            # Change HUD to red color
            # Inform : the current position of Target using function get_target_position() imported from HUD.py
            hud_color = color.red
            hud_info = HUD.get_target_position(cnt_center_x, cnt_center_y, cap_center_x, cap_center_y,
                                               cap_center_radius)

            # If Target is In Center Radius range
            # Change HUD to green color
            # Notify: Target: 'Found'
            found_cnt_center_X = cnt_center_x in range(cap_center_x - cap_center_radius, cap_center_x +
                                                       cap_center_radius)
            found_cnt_center_Y = cnt_center_y in range(cap_center_y - cap_center_radius, cap_center_y +
                                                       cap_center_radius)

            if found_cnt_center_X and found_cnt_center_Y:
                hud_color = color.green
                hud_info = 'FOUND'

            # Draw contour on Target:
            # in case rectangle target is shown on different angle
            if len(approx) == 4:
                cv2.drawContours(frame, [approx], 0, hud_color, 6)
            else:
                rect = cv2.minAreaRect(approx)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, hud_color, 6)

            # Draw circle in the center of Target
            cv2.circle(frame, (cnt_center_x, cnt_center_y), 10, hud_color, -1)

    # Draw the head up display using function create_hud() imported from HUD.py
    HUD.create_hud(frame, hud_color, cap_center_x, cap_center_y, cap_center_radius)

    # Write text in corner left of the frame
    cv2.putText(frame, "Target: {}".format(hud_info), (25, 47), cv2.FONT_HERSHEY_SIMPLEX,
                1, hud_color, 3)

    # Show the Frame
    cv2.imshow('original', frame)
    cv2.imshow('dilation', masks.get_blue_mask(frame))

    # Exit Frame with ESC key
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
