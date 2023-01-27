import classes


import socket
import os
from _thread import *

balanceTable = {}
serverClock = 0

def multi_threaded_client(connection,address):
    myClientNum = ThreadCount
    while True:
        data = connection.recv(2048)
        if not data:
            break
        data = data.decode().split(',')
        clientClock = int(data[-1])
        global serverClock
        serverClock = max(serverClock,clientClock)+1
        print("Server clock now",serverClock)
        request = data[0]
        print('Received Message: ' + classes.options[request] + ' from: ' + address[0] + ':' + str(address[1]) + "(client " + str(myClientNum) +")")
        if request == '1':
            #Check if client has sufficient balance
            clientTransferNum = data[1]
            amount = data[2]
            if int(amount) > balanceTable[myClientNum]:
                response = 'FAILED,'+str(serverClock)
            else:
                response = 'SUCCESS,'+str(serverClock)
                balanceTable[myClientNum] -= int(amount) #-1 for 0 based indexing
                balanceTable[int(clientTransferNum)] += int(amount)
            connection.sendall(str.encode(response))
            serverClock +=1 
            print("Server clock now",serverClock)

        elif request == '2':
            response = str(balanceTable[myClientNum]) + "," + str(serverClock)
            connection.sendall(str.encode(response))
            serverClock +=1 
            print("Server clock now",serverClock)

def serverInterface():
    print("Type \"print\" to see all user's balance")    
    while True:
        s = input()
        if s == "print":
            print(balanceTable)

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 65432 #non privelaged port
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))


print('Socket is listening..')
ServerSideSocket.listen(5)
start_new_thread(serverInterface,())


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    balanceTable[ThreadCount] = 10 #Initalize each client to have 10 dollars
    message = str(ThreadCount) +",10"
    Client.sendall(message.encode()) #Send the clientNumber,10 (inital balance)
    start_new_thread(multi_threaded_client, (Client,address, ))
    
    
    # start_new_thread(serverUI,())
    # print('Thread Number: ' + str(ThreadCount))
   
ServerSideSocket.close()
