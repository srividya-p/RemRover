import RPi.GPIO as GPIO
from importlib import import_module
import os
import argparse
import time
import signal
import sys

from flask import Flask, render_template, Response
from flask_ngrok import run_with_ngrok
from flask_socketio import SocketIO

if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera
    
    
def sigint_handler(signal, frame):
    GPIO.cleanup()
    print('GPIO Clean up Done.')
    os.system("sudo killall servod")
    print('Servod process terminated.')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

    
parser = argparse.ArgumentParser(description='Server for controlling RemRover')
parser.add_argument('-r','--run_remote', help = 'Use ngrok with flask to create a remote tunnel.', action='store_true')
options = parser.parse_args()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WjkdkinQk0dn63bs783nx'
socketio = SocketIO(app, async_mode=None)

if options.run_remote:
    run_with_ngrok(app)
    
#Setting start up servo positions - range from (50-250)
SERVO1 = 90
SERVO2 = 80

os.system("sudo ./servod")
time.sleep(0.005)
os.system("echo 6=%s > /dev/servoblaster"%SERVO1)
time.sleep(0.005)
os.system("echo 5=%s > /dev/servoblaster"%SERVO2)
time.sleep(0.005)

#Initialising Motors
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 38
Motor1B = 36
Motor1E = 40
 
Motor2A = 35
Motor2B = 37
Motor2E = 33
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
 
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

p1 = GPIO.PWM(Motor1E, 1000)
p2 = GPIO.PWM(Motor2E, 1000)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connected')
def handle_message(data):
    print(data['data'])
    
#SERVO CONTROLS

@socketio.on('pan_left')
def pan_left():
    global SERVO1
    if SERVO1 == 130:
        socketio.emit('p_l_limit', 'Pan Left Limit reached!')
    else:
        print('PAN LEFT COMMAND FIRED.' + str(SERVO1))
        SERVO1 += 2
        os.system("echo 6=+2 > /dev/servoblaster")
        time.sleep(0.005)

@socketio.on('pan_right')
def pan_right():
    global SERVO1
    if SERVO1 == 50:
        socketio.emit('p_r_limit', 'Pan Right Limit reached!')
    else:
        print('PAN RIGHT COMMAND FIRED.' + str(SERVO1))
        SERVO1 -= 2
        os.system("echo 6=-2 > /dev/servoblaster")
        time.sleep(0.005)
    
@socketio.on('tilt_up')
def tilt_up():
    global SERVO2
    if SERVO2 == 50:
        socketio.emit('t_u_limit', 'Tilt Up Limit reached!')
    else:
        print('TILT UP COMMAND FIRED.' + str(SERVO2))
        SERVO2 -= 2
        os.system("echo 5=-2 > /dev/servoblaster")
        time.sleep(0.005)
    
@socketio.on('tilt_down')
def tilt_down():
    global SERVO2
    if SERVO2 == 126:
        socketio.emit('t_d_limit', 'Tilt Down Limit reached!')
    else:
        print('TILT DOWN COMMAND FIRED.' + str(SERVO2))
        SERVO2 += 2
        os.system("echo 5=+2 > /dev/servoblaster")
        time.sleep(0.005)

#MOVEMENT CONTROLS

@socketio.on('stop_movement')
def stop_movement():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

@socketio.on('move_forward')
def move_forward():
    p1.start(25)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    p2.start(25)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    
@socketio.on('move_backward')
def move_backward():
    p1.start(25)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
    p2.start(25)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH) 
    
@socketio.on('move_left')
def move_left():
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    
    p1.start(25)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    
@socketio.on('move_right')
def move_right():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    
    p2.start(25)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', threaded=True)
    debug_value = False if options.run_remote else True
    socketio.run(app, host='0.0.0.0', debug=debug_value)
