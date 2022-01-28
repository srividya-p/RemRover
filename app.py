from importlib import import_module
import os
import argparse
import time

from flask import Flask, render_template, Response
from flask_ngrok import run_with_ngrok
from flask_socketio import SocketIO

if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera
    
parser = argparse.ArgumentParser(description='Server for controlling RemRover')
parser.add_argument('-r','--run_remote', help = 'Use ngrok with flask to create a remote tunnel.', action='store_true')
options = parser.parse_args()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WjkdkinQk0dn63bs783nx'
socketio = SocketIO(app, async_mode=None)

if options.run_remote:
    run_with_ngrok(app)
    
#Setting start up servo positions - range from (50-250)
SERVO1 = 100
SERVO2 = 100

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
    
@socketio.on('pan_left')
def pan_left():
    print('PAN LEFT COMMAND FIRED.')
    os.system("echo 6=-2 > /dev/servoblaster")
    time.sleep(0.005)

@socketio.on('pan_right')
def pan_right():
    print('PAN RIGHT COMMAND FIRED.')
    os.system("echo 6=+2 > /dev/servoblaster")
    time.sleep(0.005)
    
@socketio.on('tilt_up')
def tilt_up():
    print('TILT UP COMMAND FIRED.')
    os.system("echo 5=-2 > /dev/servoblaster")
    time.sleep(0.005)
    
@socketio.on('tilt_down')
def tilt_down():
    print('TILT DOWN COMMAND FIRED.')
    os.system("echo 5=+2 > /dev/servoblaster")
    time.sleep(0.005)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', threaded=True)
    debug_value = False if options.run_remote else True
    socketio.run(app, host='0.0.0.0', debug=debug_value)
