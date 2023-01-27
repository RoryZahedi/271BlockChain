import classes
import socket
import os
from _thread import *
import time

#Connect to all other clients
# echo-client.py

#Host for all clients and server is "127.0.0.1"
#Client 1 - PORT = 65551
HOST = "127.0.0.1" 
clientNumber = -1
otherClients = {'1':['2','3'],'2':['1','3'],'3':['1','2']} #What clients clientNum can send money to
clientNumberToAddress = {}
CLK = 0
import socket
def ConnectToClient(id):
    PORT = int(str(6553) + str(id))
    client_socket = socket.socket()  # instantiate
    client_socket.connect((HOST, PORT))
    print("Connected to client",id,"'s socket!")
    return client_socket

def ConnectToServer():
    PORT = 65432
    client_server_socket = socket.socket()  # instantiate
    client_server_socket.connect((HOST, PORT))
    data = client_server_socket.recv(1024).decode().split(',')
    clientNumber = data[0]
    initalBalance = data[1]
    print("Sucessfully connected to server as client",clientNumber)
    return client_server_socket,clientNumber,initalBalance

def listen():
    ServerSideSocket = socket.socket()
    host = '127.0.0.1'
    port = 65533 
    ThreadCount = 0
    try:
        ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print('Socket is listening..')
    ServerSideSocket.listen(5)
    while True:
        Client, address = ServerSideSocket.accept()
        otherClientNum = Client.recv(2048).decode()
        print('Listener connected to: ' + address[0] + ':' + str(address[1]), "(client ",otherClientNum,")")
        clientNumberToAddress[otherClientNum] = address
        start_new_thread(listenForMessages, (Client,address,otherClientNum,))
    ServerSideSocket.close()

def listenForMessages(connection,address,otherClientNum):
    #POSSIBLE MESSAGES
    #REQUEST,PID,CLK
    #REPLY,PID,CLK
    #UPDATE,STATUS
    while True:
        data = connection.recv(2048)
        global CLK
        time.sleep(3)
        if not data:
            break
        data = data.decode().split(',')
        message = data[0]
        clockReceived = data[2]
        
        if message == 'REQUEST': #update clock? respond with a REPLY
            print("Received REQUEST from client", otherClientNum)
            CLK = max(int(data[2]),CLK)+1 #Clock = max(localClock,sentClock) + 1 on receive
            print("Clock now ",CLK)
            print("Sending reply....")
            message = "REPLY," + str(clientNumber) +"," + str(CLK)
            if int(otherClientNum) == 1:
                s1.sendall(message.encode())
            else:
                s2.sendall(message.encode())
            CLK+=1
            print("Clock now ",CLK)



            desiredClient = data[3]
            amount = data[4]
            t = classes.Transaction(otherClientNum,desiredClient,amount,str(clockReceived))
            c.ClientBlockChain.insertTransaction(t)
        elif message == 'REPLY':
            print("Received REPLY from client", otherClientNum)
            CLK = max(int(data[2]),CLK)+1 #Clock = max(localClock,sentClock) + 1 on receive
            print("Clock now ",CLK)
            if otherClientNum == str(1):
                global s1Response
                s1Response = True
            else:
                global s2Response
                s2Response = True

        elif message == 'UPDATE':
            print("Received UPDATE from client", otherClientNum)
            CLK = max(int(data[2]),CLK)+1 #Clock = max(localClock,sentClock) + 1 on receive
            print("Clock now ",CLK)
            c.ClientBlockChain.setStatus(int(data[1]))

        else:
            print("unexepected message:", message)


server,clientNumber,initialBalance = ConnectToServer()

start_new_thread(listen, ())
print('Press enter to begin connecting to other clients')
input()

print("Balance  =",initialBalance)


s1 = ConnectToClient(1)
s1.sendall(str(clientNumber).encode())
s2 = ConnectToClient(2)
s2.sendall(str(clientNumber).encode())

c = classes.Client()
s1Response = False
s2Response = False

while True:
    
    print("\n\n What would you like to do? \n--------------------------\n1: Transfer \n2: Balance\n3: Print Blockchain")
    option = input()
    if option == '1': #Transfer
        #Create block in block chain
        #Make a request to all other clients <PID, Time>
        #Upon receiving replies AND if your block is head of list in block chain
            #Request server
            #Update transaction status of blockchain


        print("\nSelect from list which client you would like to transfer to:", otherClients[clientNumber])
        desiredClient = input()
        print("\nAmount:",end='$')
        amount = input()

        #Create block in block chain
        t = classes.Transaction(clientNumber,desiredClient,amount,str(CLK))
        c.ClientBlockChain.insertTransaction(t)

        #Make a request to all other clients <PID, Time>

        message = "REQUEST,"+str(clientNumber)+","+str(CLK)+","+str(desiredClient)+","+str(amount)
        s1.sendall(message.encode())
        s2.sendall(message.encode())
        CLK += 1
        print("Clock now ",CLK)
        # #Upon receiving replies AND if your block is head of list in block chain
        while True:
            if s1Response == True and s2Response == True and (int(c.ClientBlockChain.getHeadOfRequests().transaction.sender) == int(clientNumber)):
                break
         #Now can request from server
        server.sendall(','.join([option,desiredClient,amount,str(CLK)]).encode()) #sends str(option,clientNum,amnt,CLK)
        transactionStatus = server.recv(1024).decode().split(',') #SUCCESS or FAILURE
        print(transactionStatus[0])
        CLK = max(int(transactionStatus[1]),CLK)+1
        print("Clock now ",CLK)
        # #Update block and tag Abort (-1) if failed and 1 upon success, and update new head of requests
        tValue = None
        if transactionStatus[0] == "SUCCESS":
            c.ClientBlockChain.setStatus(1)
            tValue = 1
        else:
            c.ClientBlockChain.setStatus(-1)
            tValue = -1
        #Release
        message = "UPDATE,"+str(tValue)+","+str(CLK)
        s1.sendall(message.encode())
        s2.sendall(message.encode())
        CLK+=1
        print("Clock now ",CLK)
        
    elif option == '2': #Check Balance
        print('Sending request for',classes.options[option])
        message = option+','+str(CLK)
        server.sendall(message.encode())

        CLK += 1
        print("Clock now ",CLK)
        
        data = server.recv(1024).decode().split(',')
        CLK = max(int(data[-1]),CLK)+1
        print("Clock now ",CLK)
        print("Balance  =",data[0])
    elif option == '3': #Print BlockChain
        print(c.ClientBlockChain.printBlockChain())
    s1Response = False
    s2Response = False

            





# # Connect to Server
# PORT = 65432  # The port used by the server

# c = classes.Client()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     clientNumber = s.recv(1024).decode()
#     print("Sucessfully connected to server as client",clientNumber)
#     #Connect directly to other clients

#     while True:
#         print("What would you like to do? \n--------------------------\n1: Transfer \n2: Balance\n3: Print Blockchain")
#         option = input()
#         if option == '1': #Transfer
#             print("\nSelect from list which client you would like to transfer to:", otherClients[clientNumber])
#             desiredClient = input()
#             print("\nAmount:",end='$')
#             amount = input()
#             s.sendall(','.join([option,desiredClient,amount]).encode()) #sends str(option,clientNum,amnt)
#             transactionStatus = s.recv(1024).decode() #SUCCESS or FAILURE
#             print(transactionStatus)
#             t = classes.Transaction(clientNumber,desiredClient,amount)
#             c.ClientBlockChain.insertTransaction(t)

#             #Create a new block and tag Abort if failed
            
#         elif option == '2': #Check Balance
#             print('Sending request for',classes.options[option])
#             s.sendall(option.encode())
#             data = s.recv(1024).decode()
#             print("Balance  =",data)
#         else: #Print BlockChain
#             print(c.ClientBlockChain.printBlockChain())
            
