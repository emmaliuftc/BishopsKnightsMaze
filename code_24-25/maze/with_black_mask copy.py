def detect_color(image):
    colors_detected = []
    number_red_detected = 0
    number_yellow_detected = 0
    number_green_detected = 0
    number_black_detected = 0
    
    # loop to capture and process frames
    for i in range(150):
        if not image.isOpened():
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
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Capture frame
        ret, frame = image.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting...")
            break

        # Convert to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create a mask for all victim colors
        red_mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        green_mask = cv.inRange(hsv, lower_green, upper_green)
        black_mask = cv.inRange(hsv, lower_black, upper_black)
        # count number of victim colored pixels
        num_red_pixels = np.sum(red_mask1 == 255) + np.sum(red_mask2 == 255)
        num_yellow_pixels = np.sum(yellow_mask == 255)
        num_green_pixels = np.sum(green_mask == 255)
        num_black_pixels = np.sum(black_mask == 255)
        # check colored pixels and record in list
        if num_red_pixels > 5000:
            number_red_detected +=1
            if "red" not in colors_detected:
                colors_detected.append("red")
       
        if num_yellow_pixels > 5000:
            number_yellow_detected +=1
            if "yellow" not in colors_detected:
                colors_detected.append("yellow")
          
        if num_green_pixels > 5000: 
            number_green_detected +=1
            if "green" not in colors_detected:
                colors_detected.append("green")
        
        if num_black_pixels > 2000:
            number_black_detected +=1 
            if "black" not in colors_detected:
                colors_detected.append("black")
            
        # Display the original image and the mask
        # cv.imshow("Original", frame)
        # cv.imshow("Mask", red_mask1)
        
        # print(f"HSV:{hsv}")
        # print(f"Mask: {red_mask}")
        # print(f"Colors_Detected: {colors_detected}")
        
        # Exit on 'q' key press
        # if cv.waitKey(1) & 0xFF == ord('q'):
            # break

    # print(number_red_detected, number_yellow_detected, number_green_detected)
    if number_red_detected > 100:
        color = "red"
    elif number_yellow_detected > 100:
        color = "yellow"
    elif number_green_detected > 100:
        color = "green"
    elif number_black_detected > 100:
        color = "black"
    else:
        color = "none"
    # print(f"COLOR RETURNING: {color}")
    return color
