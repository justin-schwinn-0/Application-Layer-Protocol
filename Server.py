import socket
import select

HEADERSIZE = 10

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), 1234)) 
    s.listen(5)

    socketList = [s]
    clients = {}

    while True:
        readSocket, _, excepSocket = select.select(socketList, [], socketList)
        for newSocket in readSocket:
            if newSocket == s:
                clientSocket, clientAddress = s.accept()
                clientType = recieveMsg(clientSocket)
                if clientType is False:
                    print("Client has disconnected\n")
                    continue
                socketList.append(clientSocket)
                clients[clientSocket]


def recieveMsg(sock):
    try:
        fullMsg = ""
        msgLen = 0
        newMsg = True
        while True:
            msg = sock.recv(20)
            if newMsg:
                msgLen = int(msg[:HEADERSIZE])
                newMsg = False

            fullMsg += msg.decode("utf-8")

            if len(fullMsg) - HEADERSIZE == msgLen:
                print("Full message is recieved")
                return fullMsg
    except:
        return False

def sendMsg(sock, message):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(bytes(msg,"utf-8"))

def getMediaList():
    test = 1
    # Returns a string of all media in a file

if __name__ == "__main__":
    main()