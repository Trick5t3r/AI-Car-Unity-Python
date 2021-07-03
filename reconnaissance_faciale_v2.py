# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 17:37:00 2018

@author: Spyder
"""
#!/usr/bin/python3

import _thread
import threading
from threading import Lock
#import time
from time import sleep
import cv2
#import numpy as np

import socket

#global run_all, face_wanted_avance, face_wanted_rotate, do_it_respawn, lastEffectKillTheCar

record = False
lastEffectKillTheCar = 0
all_run = True
face_wanted_rotate = 0
face_wanted_avance = 0
 
# Define a function for the thread
class myThread ():#threading.Thread):
    def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.allReadyClosed = False      
      self.read_lock = Lock()
      self.frame = None
      
    def run(self):
        global all_run, face_wanted_avance, face_wanted_rotate, record
        
        #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        face_cascade = cv2.CascadeClassifier('D:\Program Files\Anaconda3\Library\etc\haarcascades\haarcascade_frontalface_default.xml')
        #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
        eye_cascade = cv2.CascadeClassifier('D:\Program Files\Anaconda3\Library\etc\haarcascades\haarcascade_eye.xml')
        
        # Create a VideoCapture object
        self.cap = cap = cv2.VideoCapture(0)
         
        # Check if camera opened successfully
        if (cap.isOpened() == False): 
          print("Unable to read camera feed")
         
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        
        if record:
            # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
            self.out = out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    

        while all_run:
          ret, frame = cap.read()
         
          if ret == True: 
            height, width, channels = frame.shape
              
            # Display the resulting frame    
            #cv2.imshow('frame',frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) #1.3 => 1.2
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.line(frame,(x+int(w/2),y+int(h/2)+10),(x+int(w/2),y+int(h/2)-10),(255,0,0),2)
                cv2.line(frame,(x+int(w/2)-10,y+int(h/2)),(x+int(w/2)+10,y+int(h/2)),(255,0,0),2)
        
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                
                if len(faces) == 1:
                    if x+w-int(width/2) > w*(2/3):
                        #print("droite")
                        face_wanted_rotate = -1
                    elif int(width/2)-x > w*(2/3):
                        #print("gauche")
                        face_wanted_rotate = 1
                    if y+h-int(height/2) > h*(2/3):
                        #print("bas")
                        face_wanted_avance = -1
                    elif int(height/2)-y > h*(2/3):
                        #print("haut")
                        face_wanted_avance = 1
                        
                    cv2.line(frame,(x+int(w/2),y+int(h/2)),(int(width/2), int(height/2)),(255,255,255),2)
                    
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
            cv2.line(frame,(int(width/2), int(height/2)+10),(int(width/2), int(height/2)-10),(0,0,0),2)
            cv2.line(frame,(int(width/2)+10, int(height/2)),(int(width/2)-10, int(height/2)),(0,0,0),2)
            
            #self.read_lock.acquire()
            cv2.imshow('frame',frame)
            #self.read_lock.release()
            
            #self.frame = frame
            
            # Write the frame into the file 'output.avi'
            if record:
                out.write(frame)
            
            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
              all_run = False
              break
         
          # Break the loop
          else:
            break 
        
        self.allReadyClosed = True
        # When everything done, release the video capture and video write objects
        cap.release()
        if record:
            out.release()
        # Closes all the frames
        cv2.destroyAllWindows()
    def join(self):
        global record
        if not self.allReadyClosed:
            self.cap.release()
            if record:
                self.out.release()
            # Closes all the frames
            cv2.destroyAllWindows()


def reset_variable():
    global do_it_respawn, lastEffectKillTheCar
    lastEffectKillTheCar = 0; #if True the car is kill
    do_it_respawn = 0

# Define a function for the thread
class myConnectionUnity (threading.Thread):
    def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.clientConnected = None
      self.s = None
      
    def run(self):
        global all_run, do_it_respawn, lastEffectKillTheCar
    
        host = 'localhost' 
        port = 50000
        backlog = 5 
        size = 1024 
        server_is_running = True
    
        reset_variable()
        nb_client_connecte_for_a_net = 1
        nb_client_already_connected_for_this_net = 0
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((host,port)) 
        s.listen(backlog)
        self.s = s
        
        print("Ready")
        while server_is_running:
            client, address = s.accept() 
            self.clientConnected = client
            print("Client connected.")
            client.send(b"0#0#")
            while 1:
                if not all_run:
                    server_is_running = False
                try:
                    data = client.recv(size).decode('utf-8')
                    #print(data)
                except ConnectionAbortedError:
                    data = "connectionAborted"
                if data == "ping":
                    client.send(b"0#0#") # rotation#avance
                elif data == "" or data == "connectionAborted":
                    if data == "":
                        self.clientConnected = None
                        client.send(b"Bye!")
                        print("Client disconnected!")
                        client.close()
                    if nb_client_already_connected_for_this_net >= nb_client_connecte_for_a_net-1:
                        server_is_running = False
                    else:
                        nb_client_already_connected_for_this_net+=1
                    break
                else:            
                    list_data = data.split("#")
                    print(list_data)
                    for i in range(0,len(list_data)):#range(0,8):
                        list_data[i] = float(list_data[i].replace(",", "."))
                        
                    # Traitement des donnees avant celle recues
                    if lastEffectKillTheCar ==0:
                        pass
                    elif lastEffectKillTheCar==1.0:
                        do_it_respawn = 1
                    #
                    if do_it_respawn:
                        reset_variable()
                        do_it_respawn = 0
                        # respawn
                        print("respawn")
                        client.send(b"127#127#")
                    else:
                        lastEffectKillTheCar = list_data[0]
                        del(list_data[0])
                            
                        message = str(face_wanted_rotate) + "#"+ str(face_wanted_avance)+"#"
                        client.send(message.encode('utf-8')) # rotation#avance
        all_run = False
    def join(self):
        if self.clientConnected:
            self.clientConnected.send(b"Bye!")
            print("Client disconnected!")
            self.clientConnected.close()
        if self.s:
            self.s.close()
"""
#try:
thread1 = myThread(1, "Thread-1")
#thread2 = myConnectionUnity(2, "Thread-2")
  
thread1.start()
#thread2.start()
#except Exception as e:
#   print ("Error: unable to start thread")
#   print(e)

while all_run:
   try:
       "print("pass")
       cv2.imshow('frame',thread1.frame)
       print("pass2")
       # Press Q on keyboard to stop recording
       if 0xFF == ord('q'):
          all_run = False
          break"
       sleep(1)
   except KeyboardInterrupt:
       print("We are stopping")
       all_run = False
       thread1.join()
       #thread2.join()
       print("Stopped")
       
thread1.join()
#thread2.join()"""
thread1 = myThread(1, "Thread-1")
thread2 = myConnectionUnity(1, "Thread-2")

thread2.start()

while all_run:
    try:
        thread1.run()
    except KeyboardInterrupt:
       print("We are stopping")
       all_run = False
       thread1.join()
       thread2.join()

all_run = False
thread1.join()
thread2.join()
    