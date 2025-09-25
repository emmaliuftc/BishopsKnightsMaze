from time import sleep
import time
import cv2
import easyocr

cap = cv2.VideoCapture(1)
reader = easyocr.Reader(['en'])

while True:
    start = time.perf_counter()
    ret, frame = cap.read()
    next_time = time.perf_counter()
    print("Time to get this frame: ", next_time - start)
    start = time.perf_counter()
    frame = cv2.resize(frame, (120,120))
    next_time = time.perf_counter()
    print("Time to resize frame: ", next_time - start)
    start = time.perf_counter()
    print("Got frame, looking for text...")
    result = reader.readtext(frame)
    next_time = time.perf_counter()
    print("Time to find letter(s): ", next_time - start)
    print(result)


cap.release()
cv2.destroyAllWindows()