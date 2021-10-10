from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

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
    sleep(3)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".jpg"):
                os.rename(filename, (shot_time + ID + ".jpg"))
                print("Renamed the jpg")
            elif filename.endswith(".nef"):
                os.rename(filename, (shot_time + ID + ".nef"))
                print("Renamed the nef")


#gp(clearCommand)

createSaveFolder()
while True:
	shot_date = datetime.now().strftime("%Y-%m-%d")
	shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	captureImages()
	renameFiles(picID)
