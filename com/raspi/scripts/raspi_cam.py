from picamera import PiCamera
from time import sleep
import datetime
import os

'''
Author: @blackram
A simple python script to interact with Raspberry Camera module
***functions***
1.it can have live preview if any external display is connected
2.it can take a picture and applies a filter
3.it can take video for given amount of time
'''

camera = PiCamera()

def get_preview(delay_time):
    os.system("/usr/bin/tvservice -p")
    camera.start_preview()
    sleep(delay_time)
    camera.stop_preview()
    os.system("/usr/bin/tvservice -o")


def get_picture():
    # camera.start_preview()
    # sleep(5)
    camera.capture('/home/pi/Scripts/photos/' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg")
    # camera.stop_preview()

def apply_filter_on_picture():
    # todo
    None


def get_video(delay_time):
    camera.start_preview()
    camera.start_recording("/home/pi/Scripts/videos/" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".h264")
    sleep(delay_time)
    camera.stop_recording()
    camera.stop_preview()


def main():
    # opens a preview when there is an physical display connected
    get_preview(10)
    # takes a picture and stores it into path mentioned
    get_picture()
    # takes video and stores into specified path
    get_video(10)


if __name__ == "__main__":
    main()
