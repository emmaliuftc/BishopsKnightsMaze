import cv2 as cv
import numpy as np

# Loop to capture and process frames
def detect_color():
    for i in range(150):
        colors_detected = []
        number_red_detected = 0
        number_yellow_detected = 0
        number_green_detected = 0

        # Initialize the camera
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        # Define color ranges (in HSV)
        lower_red1 = np.array([0, 150, 50])
        upper_red1 = np.array([10, 255, 150])
        lower_red2 = np.array([170, 150, 150]) 
        upper_red2 = np.array([179, 255, 255])
        lower_yellow = np.array([20, 80, 100])
        upper_yellow = np.array([30, 255, 255])
        lower_green = np.array([35, 80, 60])
        upper_green = np.array([85, 255, 255])

        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting...")
            break

        # Convert to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create a mask for red color
        red_mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        green_mask = cv.inRange(hsv, lower_green, upper_green)
        
        num_red_pixels = np.sum(red_mask1 == 255) + np.sum(red_mask2 == 255)
        num_yellow_pixels = np.sum(yellow_mask == 255)
        num_green_pixels = np.sum(green_mask == 255)
        
        if num_red_pixels > 5000 and "red" not in colors_detected:
            colors_detected.append("red")
            number_red_detected +=1 
        if num_yellow_pixels > 5000 and "yellow" not in colors_detected:
            colors_detected.append("yellow")
            number_yellow_detected +=1
        if num_green_pixels > 5000 and "green" not in colors_detected:
            colors_detected.append("green")
            number_green_detected += 1 
            
        # Display the original image and the mask
        # cv.imshow("Original", frame)
        # cv.imshow("Mask", red_mask1)
        
        # print(f"HSV:{hsv}")
        # print(f"Mask: {red_mask}")
        print(f"Colors_Detected: {colors_detected}")
        
        colors_detected = []
        
        # Exit on 'q' key press
        # if cv.waitKey(1) & 0xFF == ord('q'):
            # break
        print(f"num_red_detected, {number_red_detected}")
        print(f"num_yellow_detected, {number_yellow_detected}")
        print(f"num_green_detected, {number_green_detected}")

    if number_red_detected > 100:
        color = "red"
    if number_yellow_detected > 100:
        color = "yellow"
    if number_green_detected > 100:
        color = "green"
    else:
        color = "none"
    return color
    # Release the camera and close windows
    cap.release()
    # cv.destroyAllWindows()
