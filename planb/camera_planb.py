import serial

def get_data():
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        # print("Successfully connected to can on /dev/ttyACM0")
    except Exception as e:
        try:
            ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
            # print("Successfully connected to can on /dev/ttyACM1")
        except Exception as e:
            # print(f"Failed to connect to cam: {e}")
            return
    line = ser.readline().decode('utf-8').strip()
    match line:
        case "PHI":
            print("phi")
            return 2 
        case "OMEGA":
            print("omegalul")
            return 0
        case "PSI":
            print("psi")
            return 1
        case 0:
            print("target be zeroing")
            return 0
        case 1:
            print("target 1")
            return 1
        case 2:
            print("target too!")
            return 2
        case _:
            return 