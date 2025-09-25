# imports
import time
import easyocr
import cv2 as cv
import numpy as np
import os

def detect_letter():
    try:
        # reading English characters and set up image
        reader = easyocr.Reader(['en'])
        image = cv.VideoCapture(0)
        if not image.isOpened():
            print("Cannot open camera")
            exit()

        # get a frame
        start = time.perf_counter()
        ret, frame = image.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting...")
            exit()
        next_time = time.perf_counter()
        print(f"Time to get this frame: {next_time - start} seconds")

        # resize to smaller frame
        start = time.perf_counter()
        frame = cv.resize(frame, (100, 100))
        next_time = time.perf_counter()
        print(f"Time to resize frame: {next_time - start} seconds")
        
        # checked all rotations and letter is not a victim
        # look for letter
        start = time.perf_counter()
        print("Got frame, looking for text...")
        result = reader.readtext(frame)
        next_time = time.perf_counter()
        print(f"Time to find letter(s): {next_time - start} seconds")
        #print(result)
        cv.imwrite("another_captured_image.jpg", frame)
        
        if len(result) == 0:
            degrees = 0
            while degrees <= 45:
                print(degrees)
                # rotate image
                height, width = frame.shape[:2]
                center = (width // 2, height // 2)
                scale = 1.0
                M = cv. getRotationMatrix2D(center, degrees, scale)
                rotated_image = cv.warpAffine(frame, M, (width, height))
                cv.imwrite("rotated_image.jpg", rotated_image)
                # look for letter
                start = time.perf_counter()
                print("Got frame, looking for text...")
                result = reader.readtext(rotated_image)
                next_time = time.perf_counter()
                print(f"Time to find letter(s): {next_time - start} seconds")
                print(result)
                if len(result) == 0:
                    print("no letter seen")
                    letter = "nothing"
                else:
                    letter = result[0][1]
                    # check if an actual victim
                    # if letter in ("H", "S", "U"):
                        # print(f"letter:{letter}")
                        # return letter
                    # up for changing, depends how the rotations are
                degrees += 30
        else:
            letter = result[0][1]
            
        # account for rotations and return correct letter
        if letter in ("H", "I"):
            return "H"
        elif letter in ("S", "5", "0)", "6", "0"):
            return "S"
        elif letter in ("U", "3", "C"):
            return "U"
        else:
            return f"{letter} is not a victim"
            
        # Exit on 'q' key press
        #if cv.waitKey(1) & 0xFF == ord('q'):
            #exit()

    
    except IndexError:
        return "index error"
def main():
    while True:
        print(detect_letter())
    
    # Release the camera and close windows
    image.release()
    cv.destroyAllWindows()
        
main()
    

