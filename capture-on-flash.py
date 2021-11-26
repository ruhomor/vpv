from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import serial

FLASH_LEVEL = 800

shot_date = datetime.now().strftime("%Y-%m-%d") # This has been written to the while True loop.
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # This has been written to the while True loop.
picID = "PiShots"

triggerCommand = ["--trigger-capture"]
takePictureCommand = ["--capture-image-and-download"]

folder_name = shot_date + picID
save_location = "" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory.")
    os.chdir(save_location)

def captureImages():
    print("Capturing Image")
    gp(takePictureCommand)
    #sleep(3)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".jpg"):
                os.rename(filename, (shot_time + ID + ".jpg"))
                print("Renamed the jpg")
            elif filename.endswith(".nef"):
                os.rename(filename, (shot_time + ID + ".nef"))
                print("Renamed the nef")

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)


ser = serial.Serial('/dev/ttyUSB0',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE)

ser.flushInput()
ser.flushOutput()

rl = ReadLine(ser)
#gp(clearCommand)

createSaveFolder()


while True:
    raw_data = rl.readline()
    value = int(raw_data.decode())
    print(value)
    if value > FLASH_LEVEL:
        shot_date = datetime.now().strftime("%Y-%m-%d")
        shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        captureImages()
        renameFiles(picID)
        ser.flushInput()
        ser.flushOutput()
        sleep(3)
