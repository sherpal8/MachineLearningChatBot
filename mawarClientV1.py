import socket
import threading
import time # to allow short delay after sending messages
from polls.chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer  # method to train the chatbot
from polls.chatterbot.chatterbot import ChatBot # import the chatbot
import os
import mawarRecog as sr4b

# # Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('')
# hdlr = logging.FileHandler('log4mawar/log4bot.txt')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr) 

# Create the ChatBot
# Create the ChatBot
bot = ChatBot('Mawar',
    storage_adapter="polls.chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///database.db",
    # # database_uri="mysql+mysqldb://sherps:root@localhost:0/mawarKu",
    logic_adapters=[
        "polls.chatterbot.logic.MathematicalEvaluation",
        # "polls.chatterbot.logic.TimeLogicAdapter", 
        "polls.chatterbot.logic.BestMatch"
    ],
    filters=[
        "polls.chatterbot.filters.RepetitiveResponseFilter"
    ],
    preprocessors=[
        "polls.chatterbot.preprocessors.clean_whitespace"
    ]
    )

trainer = ListTrainer(bot) # set the trainer
trainer.train("polls.chatterbot.corpus.english")
for _file in os.listdir ('polls/txtTraining/'):
    chats = open ('polls/txtTraining/' + _file, 'r').readlines()
    trainer.train(chats)

alias = input("Name: ")
print ("Please speak " + alias)

# Initiate the recognizer and microphone
recognizer = sr4b.sr.Recognizer()
microphone = sr4b.sr.Microphone()

# Setting for internet protocol
tLock = threading.Lock() # to avoid program from trying to send output to screen at same time
shutdown = False # we be creating a variable called shutdown to ask the program to shutdown on exit

def receiving(name, sock): # define a thread by giving a name and a socket
    while not shutdown:
        try:
            tLock.acquire() # to acquire the lock
            while True: # try to loop forever 
                data, addr = sock.recvfrom(1024) # to grab data and address from socket.receive buffer @ 1024
                print (str(data.encode('utf-8')))
        except:
            pass # we have just passed the except parameter
        finally:
            tLock.release() # error thrown when nothing else to grab from receiving buffer= lock release and end of while loop

host = '127.0.0.1'
port = 0 # means it picks any free port on computer
server = ('127.0.0.1', 8000) # loopback address of this machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket family & type - UDP
s.bind((host, port))
s.setblocking(0) # non-blocking
rT = threading.Thread(target=receiving, args=("RecvThread",s)) # rT = receiving thread. target = to receive, s = pass through socket
rT.start() # to get rT to start

# The following loop will execute each time the user enters input
# message = input(alias + "-> ")
while True:
    message = sr4b.recognize_speech_from_mic(recognizer, microphone)
    print('You: ', message)
    response = bot.get_response(message)
    print('Bot: ', response)
    print('')

    if message != 'q': # if message is not Quit
     if message != '': # if message is not empty
# # To send data below to SQL and stratify
      strSend = alias.encode('utf-8') + ": ".encode('utf-8') + message.encode('utf-8')
      s.sendto((strSend), server) # ? how to send to SQL
# # TODO: rule out if repitition of 'message' below be the cause of slowing in reply? are codes below ok hashed out?
    # tLock.acquire()
    #  message = sr4b.recognize_speech_from_mic(recognizer, microphone) 
    # tLock.release()
    # time.sleep(0)

shutdown = True
rT.join() # wait for thread
s.close() # socket shutdown



