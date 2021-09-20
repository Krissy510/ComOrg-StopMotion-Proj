from picamera import PiCamera
from time import sleep
from gpiozero import Button, LED
from picamera.array import PiRGBArray
import cv2
import os

def captureFrame():
    global frameName
    camera.capture(f'/home/pi/Desktop/proj/animation/frame{frameName:03d}.jpg')
    print(f"Frame{frameName:03d} Taken")
    frameName += 1

# create obj
camera = PiCamera()
button = Button(17)
led = LED(21)

# Camera adjust
camera.rotation = 180
camera.resolution = (1280, 720)
camera.framerate = 32

# Set button func
button.when_pressed = captureFrame

# Create rawCapture for stream
rawCapture = PiRGBArray(camera, size=(1280, 720))

# For camera to warm up
sleep(0.1)

# file naminga
frameName = 1

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # Check if user is going to quit
    if key == ord("q"):
        break


if os.path.isfile('animation.mp4'):
    overwrite = input("Overwrite? [Y/N]")
    overwrite = overwrite.upper()
    if(overwrite == "Y"):
        os.system("rm animation.mp4")
    
if frameName > 1:
    print("Rendering....")
    os.system("ffmpeg -r 10 -i animation/frame%03d.jpg -qscale 2 animation.mp4")
    print("Finsih Render")
else:
    led = LED(20)
    print("Not enough photo")
    led.on()
delete = input("Delete all photo for process? [Y/N]")
delete = delete.upper()
if(delete == "Y"):
    print("Deleting....")
    for i in range(frameName, 0, -1):
        os.system(f"rm animation/frame{i:03d}.jpg")
    print("Deleted")
led.off()
print("Program Finished")
    


