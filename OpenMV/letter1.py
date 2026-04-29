# set up + open camera
import sensor
import math

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA) # medium resolution
sensor.skip_frames(time=2000) # allow camera to adjust

letter = "undetected"
longest = 0
second_longest = 0
longest_line = None
second_longest_line = None
while letter == "undetected":
    img = sensor.snapshot()
    # detect dark blobs
    blobs = img.find_blobs([(0,5)], pixels_threshold = 1000)
    if len(blobs) == 0:
        print("no letter found")
    else:
        print("blob found")
        for b in blobs:
            rect = b.rect()
            img.draw_rectangle(b.rect(), color = (255, 0, 0))
            circles = img.find_circles(threshold = 7000)
            # ----- detect lines (replacement for HoughLinesP) -----
            lines = img.find_lines(roi=rect, threshold=2000)
            img = img.gaussian(4)
            for l in lines:
                x1 = l.x1()
                y1 = l.y1()
                x2 = l.x2()
                y2 = l.y2()

                length = math.sqrt((x2-x1)**2 + (y2-y1)**2)

                if length > longest:
                    second_longest = longest
                    longest = length
                    longest_line = l
                    print(f"longest_line {l}")
                    print(f"longest : {longest}")
                elif length > second_longest:
                    second_longest = length
                    second_longest_line = l
                    print(f"second_longest_line{l}")
                    print(f"second_longest: {second_longest}")
                if longest!= None and second_longest_line != None:
                    img.draw_line(longest_line.line(), color=255)
                    img.draw_line(second_longest_line.line(), color=255)


        # ----- classify psi vs omega -----
        if longest > 1 and second_longest>1:
            if circles:
                letter = "omega"
            elif longest / second_longest > 1.3:
                letter = "psi"
            else:
                letter = "phi"
            print(letter)

