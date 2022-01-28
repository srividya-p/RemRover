from threading import Thread
import socket
import time
import RPi.GPIO as GPIO

VERBOSE = False
IP_PORT = 22000
P_BUTTON = 24 # adapt to your wiring

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)

def debug(text):
    if VERBOSE:
        print("Debug:---", text)

# ---------------------- class SocketHandler ------------------------
class SocketHandler(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        global isConnected
        debug("SocketHandler started")
        while True:
            cmd = ""
            try:
                debug("Calling blocking conn.recv()")
                cmd = self.conn.recv(1024)
                cmd = str(cmd, 'utf-8')
            except:
                debug("exception in conn.recv()") 
                # happens when connection is reset from the peer
                break
            debug("Received cmd: " + cmd + " len: " + str(len(cmd)))
            if len(cmd) == 0:
                break
            self.executeCommand(cmd)
        conn.close()
        print("Client disconnected. Waiting for next client...")
        isConnected = False
        debug("SocketHandler terminated")

    def executeCommand(self, cmd):
        debug("Calling executeCommand() with  cmd: " + cmd)
        if cmd[:-1] == "go":  # remove trailing "\0"
            if GPIO.input(P_BUTTON) == GPIO.LOW:
                state = "Button pressed"
            else:
                state = "Button released"
            print("Reporting current state:", state)
            state = state + "\0"
            self.conn.sendall(state.encode())
# ----------------- End of SocketHandler -----------------------

setup()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# close port when process exits:
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
debug("Socket created")
HOSTNAME = "" # Symbolic name meaning all available interfaces
try:
    serverSocket.bind((HOSTNAME, IP_PORT))
except socket.error as msg:
    print("Bind failed", msg[0], msg[1])
    sys.exit()
serverSocket.listen(10)

print("Waiting for a connecting client...")
isConnected = False
while True:
    debug("Calling blocking accept()...")
    conn, addr = serverSocket.accept()
    print("Connected with client at " + addr[0])
    isConnected = True
    socketHandler = SocketHandler(conn)
    # necessary to terminate it at program termination:
    socketHandler.setDaemon(True)  
    socketHandler.start()
    t = 0
    while isConnected:
        print("Server connected at", t, "s")
        time.sleep(30)
        t += 30