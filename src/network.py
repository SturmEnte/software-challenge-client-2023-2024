from socket import socket
from xml.etree.ElementTree import fromstring

class Connection():
    '''Connects via tcp socket to swc server on localhost 13050
    
        contains:
        self.roomId
        self.team'''
    def __init__(self, host = "localhost", port = 13050):
        self.socket = socket()
        self.socket.connect((host, port))
        
        self.roomId = None
        self.team = None
    
    def send(self, data):
        '''Send data to server'''
        self.socket.send(data.encode())
    
    def recv(self, length=1022):
        '''Receive data from server
        Optional data length parameter in int'''
        data = self.socket.recv(length).decode()
        return data
    
    def recvall(self):
        '''Receive multiple packets from server and combine them to messages'''
        data = b''
        while True:
            packet = self.socket.recv(1022)
            data += packet
            if packet[-7:] == b'</room>':
                break
        return data.decode()
    
    def join(self, reservation_code=None, room_id=None):
        '''Join a Game on localhost 13050 without roomId or reservationCode'''

        if reservation_code != None:
            self.send('<protocol><joinPrepared reservationCode="{}" />'.format(reservation_code))
        elif room_id != None:
            self.send('<protocol><joinRoom roomId="{}" />'.format(room_id))
        else:
            self.send('<protocol><join/>')

        joinedMsg = self.recv()[11:]
        self.roomId = fromstring(joinedMsg).attrib['roomId']
        
    def sendMove(self, move):
        xml = f'<room roomId="{self.roomId}"><data class="move"><actions>'
        
        for action in move.actions:
            xml += action

        xml += '</actions></data></room>'
        self.send(xml)
                
    def recvGameplay(self):
        msgs = self.recvall()
        msgs = "<wrapper>"+msgs+"</wrapper>"
        msgList = fromstring(msgs).findall('room')
        return msgList
        
        
