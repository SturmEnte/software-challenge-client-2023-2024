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

    def receive_message(self):
        self.buffer += self.receive()
        if self.buffer.startswith(b'\n  <room roomId="') and self.buffer.endswith(b"</room>"):  # Check if complete room tag is in buffer
            message = self.buffer
            self.buffer = b""
            return message
        elif self.buffer.startswith(b'\n  <left roomId="'):     # Close connection and file when "left" tag is sent from server
            self.socket.close()
            self.file.flush()
            self.file.close()
            return 0
        else:
            print("Unfinished Buffer:")
            print(self.buffer)