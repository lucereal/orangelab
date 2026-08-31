import os
import serial
from dotenv import load_dotenv
from handle_rfid import handle_uid

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")
BAUD_RATE = int(os.getenv("BAUD_RATE", "9600"))
SCANNER_ID = int(os.getenv("SCANNER_ID", "1"))

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
print(f"Listening on {SERIAL_PORT}...")

while True:
    line = ser.readline().decode("utf-8").strip()
    if line:
        print(f"UID: {line}")
        handle_uid(line, scanner_id=SCANNER_ID, source="serial")
