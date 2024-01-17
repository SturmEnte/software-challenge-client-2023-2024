from socket import socket
from xml.etree.ElementTree import fromstring

class Connection():
    '''Connects via tcp socket to swc server on localhost 13050
    
        contains:
        self.roomId
        self.team'''
    def __init__(self):
        self.socket = socket()
        self.socket.connect(('localhost', 13050))
        
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
    
    def join(self):
        '''Join a Game on localhost 13050 without roomId or reservationCode'''
        self.send('<protocol><join/>')
        joinedMsg = self.recv()[11:]
        self.roomId = fromstring(joinedMsg).attrib['roomId']
        
    def sendMove(self, move):
        if move[0] == None:
            move = f'<room roomId="{self.roomId}"><data class="move"><to x="{move[1][0]}" y="{move[1][1]}"/></data></room>'
        else:
            move = f'<room roomId="{self.roomId}"><data class="move"><from x="{move[0][0]}" y="{move[0][1]}"/><to x="{move[1][0]}" y="{move[1][1]}"/></data></room>'
        self.send(move)
                
    def recvGameplay(self):
        msgs = self.recvall()
        msgs = "<wrapper>"+msgs+"</wrapper>"
        msgList = fromstring(msgs).findall('room')
        return msgList
        
        
