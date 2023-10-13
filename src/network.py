from socket import socket
from xml.etree.ElementTree import fromstring
import datetime

class Connection():

    def __init__(self, host, port, log=False):
        self.socket = socket()
        self.socket.connect((host, port))
        
        self.roomId = None
        self.team = None

        self.buffer = b""

        self.log = log

        # Create log file
        if log:
            path = "test/log" + datetime.datetime.today().strftime("_%Y-%m-%d_%H.%M.%S") + ".xml"
            print("Log file:", path)
            self.file = open(path,"x")
            self.file.close()
            self.file = open(path,"r+")

    def join(self):
        request_xml = "<protocol><join/>"
        self.socket.sendall(request_xml.encode('utf-8'))
        joinedMsg = self.receive().decode()[11:]
        self.roomId = fromstring(joinedMsg).attrib['roomId']

    def receive(self):
        message = self.socket.recv(1022)
        if self.log and message:
            self.file.write(self.file.read() + message.decode("utf8"))
            self.file.flush()
        return message

    def receive_messages(self):
        self.buffer += self.receive()#.replace(b"\n", b"")
        if self.buffer.startswith(b'\n  <room roomId="') and self.buffer.endswith(b"</room>"):
            # print(self.buffer.decode())
            
            message = self.buffer
            self.buffer = b""
            return message
        else:
            print("Unfinished Buffer:")
            print(self.buffer)