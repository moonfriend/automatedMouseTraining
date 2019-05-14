#!/usr/bin/env python
    
import socket, select
from lib.entryDB import entryDB
import time
 
#arguments
entriesDB = entryDB();
animalNames = ['RFIDTester', 'RFIDTester2', 'RFIDTester3','RFIDTester4','M12U1A','M12U1B' , 'M12U1C','M12U1D','M12U2A' , 'M12U2B','M12U2C', 'test1','test2','test3']
sorterIP = '192.168.1.3'
sorterPrt = 5555
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
eom = "\r\n" # End Of Message 

statusSrvIP = '127.0.0.1'
statusSrvPrt = 5858

#allocations
whoIsIn = 'noOne' 
prevAnim = 'none'
connectionList = []
 
#preparing the server(s)
# srv 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((sorterIP, sorterPrt))
s.listen(1)
conn1, addr = s.accept()
connectionList.append(conn1)
print 'Sorter Connection address:', addr
#srv 2
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((statusSrvIP, statusSrvPrt))
s2.listen(1)
conn2, addr2 = s2.accept()
connectionList.append(conn2)
print 'Status server Connection address:', addr

#starting the sorter operation
data = "start\r\n"
conn1.send(data)

while 1:
     print "wait for read"
     rSock, wrSock, errSock = select.select(connectionList,[],[])
     
     if conn1 in rSock:
	print "conn1"
        data = conn1.recv(BUFFER_SIZE)
        if not data: continue
        if data == eom: continue
        if data == "\n": continue
        print "1-received data:", repr(data) ,"_EOM-" + "length: ", len(data)
        command = data.split()
        if command[0] == "in":
             print command[1] +" asked in" #TODO logfile
#             if command[1] in animalNames and command[1]!= prevAnim :
             if entriesDB.query(command[1]):
                  ans = "in " + "yes " + command[1] + eom
                  print "is allowed"
                  animalAllowed = command[1]
#             elif command[1]== prevAnim:
#		  ans = "in " + "no " + command[1] + " because repeat" + eom
#		  print "PrevAnim is here, not allowed"
#                 print "is not allowed"
	     else:
                  ans = "in " + "no " + command[1] + " because" + eom
                  print "is not allowed"
             conn1.send(ans)
	     #time.sleep(8)
 	     #ans = "in " + "no " + command[1] + " cancel" + eom
             #print "sending cancellation"
	     #ansCanc=
             #conn1.send(ans)  
        elif data == "entry completed" +eom:
             print "entry completed for " + animalAllowed
             whoIsIn = animalAllowed
             prevAnim = animalAllowed
             animalAllowed = ''
             
             # TODO maybe needs an answer to the sorter: entry yes/no
        elif data == "abort entry" + eom:
             print "entry was not successful for " + animalAllowed
             animalAllowed = ''
        elif data == "abort run" + eom:
             print "sorter asks for abort!"
        elif command[0] == "out":
             if command[1] != whoIsIn:
                  print "name mismatch, take this serious!"
             print "out succeded: " + command[1]
             whoIsIn = 'noOne'
        else:
             print "command unknown!"

     if conn2 in rSock:
         # print "conn2"
          data = conn2.recv(BUFFER_SIZE)
          print "2-received data:", repr(data) ,"_EOM-" + "length: ", len(data)
          if data == 'whoisin':
               conn2.send(whoIsIn)
               print 'whoisin answered:' + whoIsIn
          elif data == 'out':
               conn1.send('end askedBySoftware'+eom)
               print 'out request sent'

	
conn1.close()









