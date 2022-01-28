from threading import Thread
import socket, time

VERBOSE = True
IP_ADDRESS = "192.168.29.169"
IP_PORT = 22000

def debug(text):
    if VERBOSE:
        print("Debug:---", text)

# ------------------------- class Receiver ---------------------------
class Receiver(Thread):
    def run(self):
        debug("Receiver thread started")
        while True:
            try:
                rxData = self.readServerData()
            except Exception as e:
                debug("Exception in Receiver.run() - " + str(e))
                isReceiverRunning = False
                closeConnection()
                break
        debug("Receiver thread terminated")

    def readServerData(self):
        debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
                if blk != None:
                    debug("Received data block from server, len: " + \
                        str(len(blk)))
                else:
                    debug("sock.recv() returned with None")
            except Exception as e:
                raise Exception("Exception from blocking sock.recv() - " + str(e))
            data += str(blk, 'utf-8')
        print("Data received:", data)
# ------------------------ End of Receiver ---------------------

def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        cmd = cmd + "\0"
        sock.sendall(cmd.encode())
    except Exception as e:
        debug("Exception in sendCommand() - "+ str(e) )
        closeConnection()

def closeConnection():
    global isConnected
    debug("Closing socket")
    sock.close()
    isConnected = False

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debug("Connecting...")
    try:
        sock.connect((IP_ADDRESS, IP_PORT))
    except Exception as e:
        debug("Connection failed. Cause - " + str(e))
        return False
    startReceiver()
    return True

sock = None
isConnected = False

if connect():
    isConnected = True
    print("Connection established")
    time.sleep(1)
    while isConnected:
        print("Sending command: go...")
        sendCommand("go")
        time.sleep(2)
else:
    print("Connection to %s:%d failed" % (IP_ADDRESS, IP_PORT))
print("Done")