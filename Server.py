import socket
import select

HEADERSIZE = 10

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), 1249)) 
    s.listen(5)

    socketList = [s] # This is probably unecessary, but storing the list of all connected clients for now
    clients = {}

    while True:
        print("Running server")
        readSocket, _, excepSocket = select.select(socketList, [], socketList)
        for sock in readSocket:
            if sock == s:
                clientSocket, clientAddress = s.accept()
                print("client has been accepted") # Just for testing
                clientType = recieveMsg(clientSocket)
                print(clientType) # Just for testing
                if clientType == False:
                    print("Client has disconnected\n")
                    continue
                socketList.append(clientSocket)
                clients[clientSocket] = clientType
                #print statement kinda iffy, fix or delete
                #print('Accepted connection from {}:{}, From: {}'.format(*clientAddress, clientType['data'].decode('utf-8')))
            else:
                message = recieveMsg(sock)

                if message == False:
                    #print statement kinda iffy, fix or delete
                    #print('Closed connection from: {}'.format(clients[sock]['data'].decode('utf-8')))
                    print("Connection was forcibly closed")
                    socketList.remove(sock)
                    del clients[sock]
                    continue
                elif message.lower() == "sendlist":
                    sendMsg(sock, getMediaList())
                elif message.lower() == "pause": # Figure out how to do this
                    break
                elif message.lower() == "resume": # Figure out how to do this
                    break
                elif message.lower() == "restart": # Figure out how to do this
                    break
                else: # If none of the previous messages match, assume that message is filename to be rendered
                    break # send stream to renderer if file found, else send invalid to renderer



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
                return fullMsg[HEADERSIZE:]
    except:
        return False

def sendMsg(sock, message):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(bytes(msg,"utf-8"))

def getMediaList():
    return "List"
    # Returns a string of all media in a file

def getFile(filename):
    return "Bytestream of file"

if __name__ == "__main__":
    main()