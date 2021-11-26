from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray
import cv2
import os

def captureFrame():
    global frameName
    camera.capture(f"/home/pi/Desktop/proj/animation/frame{frameName:03d}.jpg")
    print(f"Frame{frameName:03d} Taken")
    frameName += 1

def endProgram():
    print("Program End")
    exit(0)


# file name number
frameName = 1
foldername = "animation"

usin = int(input("1\tTake a photo\n2\tCreate a video directly\n"))
if usin == 1:
    # create obj
    camera = PiCamera()

    # Camera adjust
    camera.rotation = 180
    camera.resolution = (1280, 720)
    camera.framerate = 32

    # Create rawCapture for stream
    rawCapture = PiRGBArray(camera, size=(1280, 720))

    # For camera to warm up
    sleep(0.1)


    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        
        # Check if user is going to quit
        if key == ord("q"):
            cv2.destroyAllWindows()
            usin = input("Create a video? [Y/N]").upper().replace(" ", "")
            if(usin == "N"):
                endProgram()
            break
        elif key == ord("p"):
            captureFrame()
            
vidName = input("Video name?: ")
if os.path.isfile(f'{vidName}.mp4'):
    print(f"{vidName}.mp4 already existed")
    overwrite = input("Overwrite? [Y/N]").upper().replace(" ","")
    if(overwrite == "Y"):
        os.system(f"rm {vidName}.mp4")
    else:
        endProgram()

frameAM = int(input("Frame?: "))
print("Rendering....")
os.system(f"ffmpeg -r {frameAM} -i {foldername}/frame%03d.jpg -qscale 2 {vidName}.mp4")
print("Finish Render")
usin = input("Open Video?[Y/N]: ").upper().replace(" ","")
if usin == "Y":
    os.system(f"vlc {vidName}.mp4")
else:
    print("Not enough photo")
delete = input("Delete all photo taken? [Y/N]")
delete = delete.upper()
if(delete == "Y"):
    print("Deleting....")
    for i in range(frameName, 0, -1):
        os.system(f"rm animation/frame{i:03d}.jpg")
    print("Deleted")
endProgram()
    


