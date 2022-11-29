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
        for sock in readSocket:
            if sock == s:
                clientSocket, clientAddress = s.accept()
                clientType = recieveMsg(clientSocket)
                if clientType == False:
                    print("Client has disconnected\n")
                    continue
                socketList.append(clientSocket)
                clients[clientSocket] = clientType
                print('Accepted connection from {}:{}, From: {}'.format(*clientAddress, clientType['data'].decode('utf-8')))
            else:
                message = recieveMsg(sock)
                
                if message == False:
                    print('Closed connection from: {}'.format(clients[sock]['data'].decode('utf-8')))
                    socketList.remove(sock)
                    del clients[sock]
                    continue
                elif message.lower() == "sendlist":
                    break
                elif message.lower() == "render": # Figure out how to do this
                    break
                elif message.lower() == "pause": # Figure out how to do this
                    break
                elif message.lower() == "resume": # Figure out how to do this
                    break
                elif message.lower() == "restart": # Figure out how to do this
                    break



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