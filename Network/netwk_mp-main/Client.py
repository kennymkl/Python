import socket
import threading
import json
import time

encoding = 'utf-8'
bufferSize = 1024          
global serverAddressPort
joined = False



def printFromServer(bytesAddressPair):
    if not joined:
        return
    convMsg = str(bytesAddressPair[0], encoding)
    jsonMsg = json.loads(convMsg)
    serverMsg = "\n{}".format(jsonMsg["message"])
    print(serverMsg)

def joinComm(userCommand):
    
    try:
        wholeCommand = str.split(userCommand," ")
        if len(wholeCommand) != 3:
            raise ValueError("Invalid number of parameters for /join command.")
        
        if wholeCommand[1] != "127.0.0.1":
            raise ValueError("Invalid IP address. Only connections from localhost are allowed.")
        
        if wholeCommand[2] != "12345":
            raise ValueError("Invalid port number. Please use correct port number.")

        jsonFormat =  { "command":wholeCommand[0]}

        # convert into JSON:
        y = json.dumps(jsonFormat)
        bts = str.encode(y)                                 # Bytes to Send
        sap = (wholeCommand[1], int(wholeCommand[2]))       # Server Address Port

        

        return bts, sap
    
    except ValueError as e:
        print("Error: " + str(e))
        return None, None
    except:
        print("Error: Command parameters do not match or is not allowed.")
        return None, None

def leaveComm(userCommand):
    jsonFormat =  { "command":userCommand}

    # convert into JSON:
    y = json.dumps(jsonFormat)
    bytesToSend = str.encode(y)

    return bytesToSend

def regComm(userCommand):
    wholeCommand = str.split(userCommand," ")
    jsonFormat =  { "command":wholeCommand[0], "handle":wholeCommand[1]}

    # convert into JSON:
    y = json.dumps(jsonFormat)
    bts = str.encode(y)                                 # Bytes to Send

    return bts

def msgComm(userCommand):
    try:
        wholeCommand = str.split(userCommand," ",2)
        print(wholeCommand)
        jsonFormat =  { "command":wholeCommand[0], "handle":wholeCommand[1], "message":wholeCommand[2]}

        # convert into JSON:
        y = json.dumps(jsonFormat)
        bts = str.encode(y)                                 # Bytes to Send

        return bts
    except:
        return None
def allComm(userCommand):
    try:
        wholeCommand = str.split(userCommand," ",1)
        jsonFormat =  { "command":wholeCommand[0], "message":wholeCommand[1]}

        # convert into JSON:
        y = json.dumps(jsonFormat)
        bts = str.encode(y)                                 # Bytes to Send

        return bts
    except:
        return None


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)



while (joined==False):
    userStartCommand = input("Enter command: ")
    if "/join" in userStartCommand:
        try:
            bytesToSend, serverAddressPort = joinComm(userStartCommand)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            joined = True

        except:
            print("Error: Connection to the Message Board Server has failed!")
    else:
        print("Error: Command not found.")



# Listen for incoming datagrams
def sender():
    global Registered
    Registered = False
    global serverAddressPort
    global joined

    while True:
        userCommand = input("Enter command: ")

        if "/join" in userCommand:
            try:
                joined = True
                bytesToSend, serverAddressPort = joinComm(userCommand)

                # Send to server using created UDP socket
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            except:
                print("Error: Connection to the Message Board Server has failed!")


        elif "/leave" in userCommand:
            if joined:
                bytesToSend = leaveComm(userCommand)
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)
                joined = False  # set joined flag to False
            else:
                print("Error: Disconnection failed. Please connect to the server first.")
            joined = False 
            
        elif "/register" in userCommand:
            if Registered == False:
                Registered = True
                bytesToSend = regComm(userCommand)
                # Send to server using created UDP socket
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            else:
                print("This Client is already Registered.")
            
  #     elif "/register" in userCommand:
  #          Registered = True
  #          bytesToSend = regComm(userCommand)
  #          if bytesToSend is not None:
  #              # Send to server using created UDP socket
  #              UDPClientSocket.sendto(bytesToSend, serverAddressPort)
  #          else:
                print("Error: Command parameters do not match or is not allowed.")

        elif "/msg" in userCommand:
            bytesToSend = msgComm(userCommand)
            if bytesToSend is not None:
                # Send to server using created UDP socket
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            else:
                print("Error: Command parameters do not match or is not allowed.")

                
        elif "/all" in userCommand: 
            bytesToSend = allComm(userCommand)
            if bytesToSend is not None:
                # Send to server using created UDP socket
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            else:
                print("Error: Command parameters do not match or is not allowed.")

        elif "/?" in userCommand:
            print("------COMMANDS ------")
            print("Connect to the server application: /join <server_ip_add> <port>")
            print("Disconnect to the server application: /leave")
            print("Register a unique handle or alias: /register <handle>")
            print("Send a private message: /msg <handle> <message>")
            print("Send a message to all connected clients: /all <message>")
            print("List all connected clients: /list")
            print("To display help for the commands: /?")
        else:
            print("Error: Command not found.")

        time.sleep(1)

def receiver():

    while(True):
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize) # Receive from Server a tuple (bytes, address)
        printFromServer(bytesAddressPair)

receive = threading.Thread(target=receiver)
send = threading.Thread(target=sender)

if (joined==True):
    print("Thread started")
    receive.start()
    send.start()
