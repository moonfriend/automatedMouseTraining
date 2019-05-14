#!/usr/bin/env python3
import pdb
from oct2py import octave
import socket
import select
import time
import logging
from lib.entryDB import entryDB

#octave.addpath('.')
##octave.Bpod('cli',anim,'C0rd_middle_RL_AUD')
BUFFER_SIZE=1024;
statusSrvIP = '127.0.0.1'
statusSrvPrt = 5858
entriesDB = entryDB();

logging.basicConfig(filename='example2.log',level=logging.INFO,format='%(asctime)s %(message)s')
logging.basicConfig(format='%(asctime)s %(message)s')

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((statusSrvIP,statusSrvPrt))
logging.info("connected")

noOne = b'noOne'
anim = noOne;
prevAnim = noOne;

while True:
    time.sleep(20)
    try:
        s2.send(b'whoisin');
        anim=s2.recv(1024)#check success
        
        if anim == noOne:
            prevAnim = noOne
           
            continue            
        elif anim == prevAnim:
            logging.warning('anim is prevanim:' + anim.decode("utf-8"))
            logging.info ('animal being sent out')
            s2.send(b'out')#check success
            octave.Bpod('cli','test1','soundKick')
            octave.eval("clear('BpodSystem')")
            logging.info('tried to kick out with sound')
            logging.info('out request sent to server')
        else:
       	    # if anim != prevAnim:
            logging.info(' going to play:' + anim.decode("utf-8"))
            nextDate= octave.Bpod('cli',anim,'BimodalAttention')
            print('next Date from Bpod: ' + str(nextDate))
            print('Going to write to DB')
            entriesDB.assignNextDate(anim.decode("utf-8"), nextDate) 

            octave.eval("clear('BpodSystem')")
            logging.info ('Bpod Finished;animal being sent out')
            s2.send(b'out')#check success
            print('now query')
            entriesDB.query(anim.decode("utf-8"))
            entriesDB.query(anim)
# lights on here TODO
            logging.info('out request sent to server')
            prevAnim = anim;
    except Exception as e:
        logging.error('there was an error '+ str(e))
