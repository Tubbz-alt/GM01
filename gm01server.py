import socket
import sys
import thread
import time
import datetime
import os
import threading
import subprocess
import logging


#logging.basicConfig(format="%(asctime)s %(message)s",level=logging.DEBUG)
logging.basicConfig(filename='system.log',format="%(asctime)s %(message)s",level=logging.DEBUG)

if not os.path.exists('dev'):
    os.makedirs('dev')
if not os.path.exists('fotos'):
    os.makedirs('fotos')

def clientthread(clientsocket):
  filemap={}
  while True:
    input = clientsocket.recv(4096)
    if not input:
      clientsocket.shutdown(socket.SHUT_RD)
      break;
    else:
      #print "Resived:"
      #print(input)
      hexs= []
      for ch in input:
        hv= hex(ord(ch)).replace('0x','')
        if len(hv)==1:
          hv='0'+hv
        hexs.append(hv) 
      #print reduce(lambda x,y:x+y, hexs)
      #print "Start Bit:       " + hexs[0]+hexs[1];      
      #print "Content Length:  " + hexs[2]+hexs[3];
      #print "Reserved Bit:    " + hexs[4]+hexs[5];      
      #print "IMEI No(8):      " + str(hexs[6:14]);      
      #print "ISerial Number:  " + hexs[14]+hexs[15];      
      #print "Protocol Number: " + hexs[16];      
      #print "End Bit:         " + hexs[-2]+hexs[-1];      
      #print "Length:          "+ str(len(input))+ "  = "+str(ord(input[2])*255+ord(input[3])+6)         
      
      output=''
      
      #show that a device is alive!
      subprocess.check_output(['touch', 'dev/'+reduce(lambda x,y:x+y, hexs[6:14])])

      if ord(input[16])== 0x56:
        logging.info(reduce(lambda x,y:x+y, (hexs[6:14]))+".......Send command to device .............")   
        #print "Command Serial No.(4)  "+str(hexs[17:21])
        #print "Processing Result(1)  "+hexs[21]
        #print "Content replied (?):  "+input[22:-2]
        #no respons:

      if ord(input[16])== 0x4e:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Time synchronous ............."   )   
        #build respons:
        now = datetime.datetime.utcnow()      #Time of Server(6)  Format: yymmddhhMMSs UTC time
        output+=chr(now.year-2000)
        output+=chr(now.month)
        output+=chr(now.day)
        output+=chr(now.hour)
        output+=chr(now.minute)
        output+=chr(now.second)

      if ord(input[16])== 0xa0:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Register Request ............."   )   
        #print "Terminal Software Version No.:  "+input[17:39]
        #print "Contry Code:                    "+hexs[40]+hexs[41]
        #print "Network Operator Code:          "+hexs[42]
        #print "Region Code:                    "+hexs[43]+hexs[44]
        #print "Base Station Identity Code:     "+hexs[45]+hexs[46]+hexs[47]
        #build respons:
        output+=input[6:14];                  #Terminal ID(8)
        output+=chr(0x12)+chr(0x34)+chr(0x56) #Password(3)
        output+=(chr(0x00)*20)                #Username(20)
        output+=chr(0x00)                     #Type of User(1)
        now = datetime.datetime.utcnow()      #Time of Server(6)  Format: yymmddhhMMSs UTC time
        output+=chr(now.year-2000)
        output+=chr(now.month)
        output+=chr(now.day)
        output+=chr(now.hour)
        output+=chr(now.minute)
        output+=chr(now.second)
        
      if ord(input[16])== 0xa1:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......User Login ............."  )    
        #print "Password:                       "+str(hexs[17:29])
        #print "Terminal Type:                  "+hexs[29]
        #print "Terminal Software Version No.:  "+input[30:52]
        #print "Contry Code:                    "+hexs[52]+hexs[53]
        #print "Network Operator Code:          "+hexs[54]
        #print "Region Code:                    "+hexs[55]+hexs[56]
        #print "Base Station Identity Code:     "+hexs[57]+hexs[58]+hexs[59]
        #build respons:
        output+=chr(0x00);                    #Result of verifying(1)
        output+=input[6:14];                  #Terminal ID(8)
        output+=(chr(0x00)*20)                #Username(20)
        output+=chr(0x00)                     #Type of User(1)
        now = datetime.datetime.utcnow()      #Time of Server(6)  Format: yymmddhhMMSs UTC time
        output+=chr(now.year-2000)
        output+=chr(now.month)
        output+=chr(now.day)
        output+=chr(now.hour)
        output+=chr(now.minute)
        output+=chr(now.second)

      if ord(input[16])== 0xa2:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Upload location ............." )     
        #print "Information Content(24):        "+str(hexs[17:41])
        #print "Contry Code:                    "+hexs[41]+hexs[42]
        #print "Network Operator Code:          "+hexs[43]
        #print "Region Code:                    "+hexs[44]+hexs[45]
        #print "Base Station Identity Code:     "+hexs[46]+hexs[47]+hexs[48]
        #print "Voltage class:                  "+hexs[49]
        #print "GSM signal strength:            "+hexs[50]
        #print "Location status:                "+hexs[51]
        #print "Number of satellite:            "+hexs[52]
        #print "Satellite SNR:                  "+str(hexs[53:65])
        #print "Temperature:                    "+hexs[65]+hexs[66]
        #print "Pressure:                       "+str(hexs[67:71])
        #print "Altitude:                       "+str(hexs[71:75])
        #build respons:
        output+=chr(0x00);                    #Result of verifying(1)

      if ord(input[16])== 0xa6:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Upload Picture............."  )    
        #print "location status(1)              "+hexs[17]
        #print "Longitude(4)                    "+str(hexs[18:22])
        #print "Latitude(4)                     "+str(hexs[22:26])
        #print "Country Code(2):                "+hexs[26]+hexs[27]
        #print "Network Operator code(1):       "+hexs[28]
        #print "Region Code(2):                 "+hexs[29]+hexs[30]
        #print "Base station identity code(3):  "+hexs[31]+hexs[32]+hexs[33]
        #print "Photo type(1):                  "+hexs[34]
        #print "Content of words (50):          "+input[35:85]
        #print "Photographing time(6):          "+str(hexs[86:92])
        #build respons:
        output+=(chr(0x00)*4);                #Processing time(4)
        output+=input[12:14]+input[86:92];    #Photo file KEY(8)
        #prepair for new File
        filemap={}
        
      if ord(input[16])== 0xa7:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Picture details............."   )   
        #print "Package Serial No.              "+hexs[17]+hexs[18]
        #print "End or not                      "+hexs[19]
        #print "Photo fileKEY:                  "+str(hexs[20:28])
        #print "Size of uploaded file:          "+str(hexs[28:32])
        #print "Data:                           "
        #print str(hexs[32:-2])
        #build respons:
        output+=input[18]+input[17];          #Package Serial No.(2)
        output+=chr(0x00);                    #Processing result(1)
        output+=(chr(0x00)*4);                #Processing time(4) 
        #Save contant:
        filemap[ord(input[17])+ord(input[18])*256]=input[32:-2];
        if ord(input[19])==1:
          #Save File:
          logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Save File to Drive............."   )  
          filename= "fotos/"+reduce(lambda x,y:x+y, hexs[20:28])+'.png'
          f = open(filename, 'wb');
          for i in range(0, ord(input[17])+ord(input[18])*256+1):
            if i in filemap:
              f.write(filemap[i])
          f.close()
          #upload
          result = subprocess.check_output(['gdrive', 'upload', filename])
          logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+result)
          filemap={}
          
        
      if ord(input[16])== 0xa9:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Upload alarm info............."   )   
        #no respons
        
        
      if ord(input[16])== 0xac:
        logging.info( reduce(lambda x,y:x+y, (hexs[6:14]))+".......Upload parameters............."    )  
        #print "Parameters detail:              "+input[17:-2]
        #build respons:
        output+=chr(0x01);                    #Processing result(1)
        output=''  #do not respons! camera will reconnect ...
        
      if output!='':
        olength= len(output)+3;
        ostart=chr(0x68)+chr(0x68)                 #Start Bit(2)
        ostart+=chr(olength/256)+chr(olength%256)  #Content Length(2)
        ostart+=input[14:16]                       #Information Serial Number(2)
        ostart+=input[16]                          #Protocol Number(1)
        output=ostart+output
        output+=chr(0x0d)+chr(0x0a)                #End Bit(2)
        hexs= []
        for ch in output:
          hv= hex(ord(ch)).replace('0x','')
          if len(hv)==1:
            hv='0'+hv
          hexs.append(hv) 
        #print "Respons:"
        #print reduce(lambda x,y:x+y, hexs)
        clientsocket.send(output)
        
        
        
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('', 8710))
serversocket.listen(5)
logging.info( "Wait for connecttion on ...")

while True:
  (clientsocket, address) = serversocket.accept()
  logging.info( "New Connection: "+str(address))
  t = threading.Thread(target=clientthread, args=(clientsocket,))
  t.daemon= True
  t.start()
  
