import os
import time

SERVO1 = 90
SERVO2 = 80

print('Stting Servo to 90, 80.')

os.system("sudo ../servod")
time.sleep(0.005)
os.system("echo 6=%s > /dev/servoblaster"%SERVO1)
time.sleep(0.005)
os.system("echo 5=%s > /dev/servoblaster"%SERVO2)
time.sleep(0.005)

os.system("sudo killall servod")
print('Servod process terminated.')
