import socket 
import time

host = '127.0.0.1'
port = 8000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # utilising UDP protocol i.e. datagram
s.bind((host,port))
s.setblocking(0) # sets socket as non-blocking i.e. always to grab data from screen

quitting = False # not trying to Quit
print ("Server Started.")

while not quitting:
    try:
        data, addr = s.recvfrom(1024) # server receive data from client (1024 bytes)
        if "Quit" in str(data):
            quitting = True # if client sent Quit data, then to Quit 
        if addr not in clients: # if address received not already in client list
            clients.append(addr) # then to append client address to list    
        print ((time.ctime(time.time()) + str(addr) + ": :" + str(data)))
        for client in clients: # for the client(s) in client list
            s.sendto(data.encode('utf-8'), client) # to send the data back to the client(s)-> ? innovate to send data to SQL
    except:
        pass
s.close()