import socket
import select
import os

HEADERSIZE = 10
DEFAULT_SEG_SIZE = 256

def main():

    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), 31249)) 
    s.listen(5)

    socketList = [s] # This is probably unecessary, but storing the list of all connected clients for now
    clients = {}

    while True:
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
                
                msgsplits = message.split(" ")
                cmd = msgsplits[0].lower()
                content = msgsplits[1:]

                if cmd == "list":
                    
                    sendMsg(sock, getMediaList())
                    #sendMsg(sock, "Example list")
                    
                elif cmd == "read": # format of read is 'read <file name> <byte offeset>'
                    
                    print(content)

                    data = getMediaChunk(content[0],int(content[1]))
                    sendMsg(sock,data)
                    
                else: # If none of the previous messages match, assume that message is filename to be rendered
                    print("Unknown command") # send stream to renderer if file found, else send invalid to renderer



def recieveMsg(sock:socket.socket)-> str:
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
                return fullMsg[HEADERSIZE:]
    except:
        return False

def sendMsg(sock:socket.socket, message):
    print(f"sending: {message}")
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(msg.encode())

def getMediaList()-> str:
    
    fileList = os.listdir('files')

    dataList = ""

    #print(fileList)

    for str in fileList:
        dataList += str + "\n"
    #print(dataList)

    #print(f"sending list of {len(dataList)}...")

    return dataList
    # Returns a string of all media in a file
def getMediaChunk(filename:str, offset:int = 0)-> str :
    data = getFile(filename)

    start = offset if offset < len(data) else len(data)
    end = offset + DEFAULT_SEG_SIZE if(offset + DEFAULT_SEG_SIZE < len(data)) else len(data)

    print(f"Start: {start}, End: {end}")

    asdjha = data[start:end]
    return asdjha

def getFile(filename :str):

    fileList = os.listdir('files')

    if(filename in fileList):

        print(f"File \'{filename}\' found...")
        path = "files/"+filename
        data = open(path).read()
        print(f"File of {len(data)} bytes")
        return data
    else:
        return "File not found"
                    


if __name__ == "__main__":
    #print(getMediaList())
    #print(getFile('stuff.txt'))
    #print()
    #print(getMediaChunk("stuff.txt"))
    main()