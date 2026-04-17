import serial
import time

PORT = "/dev/ttyACM0"   # Linux (Docker)
BAUD = 115200

while True:
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            print(f"Connected to Pico on {PORT}")

            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if line:
                    print(f"PICO: {line}")

    except Exception as e:
        print(f"Serial error: {e}")
        time.sleep(2)