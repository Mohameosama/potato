import socket

class ClientSock():

    HEADERSIZE = 20

    def __init__(self, ip, port):
        self.PORT = port
        self.IP = ip
        # self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.IP, self.PORT))

    def sendMsg(self, msg):
        data = f'{len(msg):<{self.HEADERSIZE}}'+ msg
        codedMsg = bytes(data, "utf-8")
        self.clientSocket.send(codedMsg)
        
    def recvMsg(self):

        fullMsg = ''
        newMsg = True

        while True:

            msg = self.clientSocket.recv(self.HEADERSIZE+5)

            # if msg start then get it's len from the header
            if newMsg:
                decodedMsg = msg[:self.HEADERSIZE].decode("utf-8")
                msgLen = int(decodedMsg)
                newMsg = False

            fullMsg += msg.decode("utf-8")

            if len(fullMsg)-self.HEADERSIZE == msgLen:
                newMsg = True
                break
            
        fullMsg = fullMsg[self.HEADERSIZE:]
        flag = fullMsg[-1]
        response = fullMsg[:-1]
        return response, flag

    def close(self):
        self.clientSocket.close()
