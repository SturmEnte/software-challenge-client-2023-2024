from socket import socket
from xml.etree.ElementTree import fromstring

class Connection():

    def __init__(self, host, port):
        self.socket = socket()
        self.socket.connect((host, port))
        
        self.roomId = None
        self.team = None

    def join(self):
        request_xml = "<protocol><join/>"
        self.socket.sendall(request_xml.encode('utf-8'))

    def receive_messages():
        pass