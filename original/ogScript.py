from picamera import PiCamera
from time import sleep
from gpiozero import Button

# initialize
button = Button(17) # Button at connect at pin 17
camera = PiCamera() # Create PiCamera
frame = 1 # Initialze frame name

# Rotate camera so it position correctly
camera.rotation = 180

# Start camera
camera.start_preview()

try:
    while True:
        button.wait_for_press()
        camera.capture(f'/home/pi/Desktop/original/photo/frame{frame:03d}.jpg')
        print(f"Captured frame{frame:03d}")
        frame += 1
except KeyboardInterrupt:
    print("Program Stop")
    camera.stop_preview()
