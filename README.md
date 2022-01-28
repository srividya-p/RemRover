# RemRover

RemRover is an easy to control surveillance vehicle that continually transmits the video footage of the area it is exploring. The user has full control over the 
movement of the rover through a socket based web interface. The camera module on the rover is supplemented with a pan and tilt mechanism that allows a 360 
degree view. 

<img align="right" src="https://user-images.githubusercontent.com/74781344/151489411-dbec2c7e-0532-407a-a16a-45ae372b0cf4.jpg">

#### Remote Controlled Rover built with - ####
1. Raspberry Pi3B+
2. Raspberry Pi Camera Module V 2.1
3. 2 S690 Tower Pro Micro Servos
4. Pan & Tilt Bracket 
5. DC Motors 
6. 2WD Smart Robot Car Chassis 

#### Controlled by a Web Interface built with - ####
1. Python Flask - Serving web page
2. Flask SocketIO - Fast bi-directional communication for running commands
3. ngrok - Exposing the interface through a tunnel for remote accesss
4. HTML/CSS/JS - Minimalistic vanilla frontend 


### Code setup can be done on a Raspberry Pi as follows - ### 

_**Note** - A vitrual env can be created before running the following command._

```
pip3 install -r requirements.txt
```

Running the server with access only on local network - 

```
python3 app.py
```

Running the server with remote access - 

```
python3 app.py --remote_run
```
