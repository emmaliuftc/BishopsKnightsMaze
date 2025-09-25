import time
from time import sleep
import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
print(sys.path)


import cv2 
import numpy as np #NumPy is library for arrays/matrices and numerical computing: as np is just a short cut for np.array() which is just a function 

#runs function with parameter called image 
def detect_colors(image):
    # Convert image to HSV color space
    #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #sets up empty list: detected_colors
    detected_colors = []
    #looping through color with lower/upper bounds in COLOR_RANGES so returns key-value pairs like [(0, 120, 70), (10, 255, 255)]
    for color, (lower, upper) in COLOR_RANGES.items():
        #seperates the key-value pairs into seperate lists labeled lower_bound and upper_bound
        lower_bound = np.array(lower, dtype=np.uint8) #a np.array returns 8 digit arrays bc its easier to srotre or smthing 
        upper_bound = np.array(upper, dtype=np.uint8)
        
        # Create a mask for the color (basically a binary mask where everything in the range between lower and upper bound is white and everything outside is black)
        # helps to isolate and make cv2 concentrate better
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        
        # Check if color is detected (basically if the number of white pixels exceeds 500)
        if cv2.countNonZero(mask) > 500:  
            detected_colors.append(color) #then appends the color to the list 
            
            # Draw a contour around detected color (like a boundary: might not need cuz usually for shapes) : RETR_TREE is for nested objects like a hole in a color and CHAIN_APPROX_SIMPLE is removing not needed points (just cleaning it up)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
            # draw contours on image with (-1 (just means draw all contours), 255's --> just white, and 2 pixel thickness)
            cv2.drawContours(image, contours, -1, (255, 255, 255), 2)
    #returns list and image
    return detected_colors, image

# If you want to see more of what you can do, un-comment help(cam).
# Notice that many of the methods there just save the images/video to file.
# help(cam)

# It takes (literally) a second for the camera to start up.  Wait for it...
sleep(1)

image = cv2.VideoCapture(0)
# get a frame
start = time.perf_counter()
ret, frame = image.read()
next_time = time.perf_counter()
print(f"Time to get this frame: {next_time - start} seconds")

# resize to smaller frame
start = time.perf_counter()
frame = cv2.resize(frame, (120,120))
next_time = time.perf_counter()
print(f"Time to resize frame: {next_time - start} seconds")
# Define color ranges in HSV (Hue: color type, Saturation: intensity/purity of the color, Value: brightness (like black is 0% brightness))
COLOR_RANGES = {
    "red": [(0, 120, 70), (10, 255, 255)],  # ranges in HSV for red
    "yellow": [(20, 100, 100), (30, 255, 255)],  # ranges in HSV for yellow
    "green": [(40, 50, 50), (90, 255, 255)],  # ranges in HSV for green
    "black": [(0, 0, 0), (180, 255, 50)],  
    "silver": [(0, 0, 180), (180, 20, 230)], 
    "blue": [(90, 50, 50), (130, 255, 255)], 
}

#image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#cv2.imshow("Test", image)
cv2.waitKey(0)
# Load image (or use webcam)
#image = cv2.imread(image)  # Replace with your image path
if image is None:
    print("Error: Image not found.")
else:
    #sets variables detected and output image based on returns from the function 
    detected, output_image = detect_colors(image)

    #outpute colors
    print("Detected colors:", detected)
    #outpute images
    #cv2.imshow("Color Detection", output_image)
    #wait until hit key to close the window 
    cv2.waitKey(0)
    cv2.destroyAllWindows()#close windows that were opened (the image)
