from time import sleep
from smbus2 import SMBus
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import serial

FLASH_LEVEL = 900

shot_date = datetime.now().strftime("%Y-%m-%d") # This has been written to the while True loop.
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # This has been written to the while True loop.
picID = "PiShots"

triggerCommand = ["--trigger-capture"]
takePictureCommand = ["--capture-image-and-download"]

folder_name = shot_date + picID
save_location = "" + folder_name

SLAVE_ADDRESS = 0x04
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

def request_reading():
    reading = bus.read_i2c_block_data(i2c_addr=SLAVE_ADDRESS,
            register=0x00, length=2)
    return (reading[0] * 256 + reading[1])

createSaveFolder()

bus = SMBus(1)

while True:
    value = request_reading()
    print(value)
    if value > FLASH_LEVEL:
        if value > 30000:
            continue
        shot_date = datetime.now().strftime("%Y-%m-%d")
        shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        captureImages()
        renameFiles(picID)
        sleep(3)
