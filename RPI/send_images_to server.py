import socket 
import numpy as np
import cv2
from queue import Queue
from _thread import *

enclosure_queue = Queue()


def webcam(queue):
    capture = cv2.VideoCapture(0) 

    while True:
        ret, frame = capture.read()

        if ret == False:
            continue


        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] # Set image quality
        result, imgencode = cv2.imencode('.jpg', frame, encode_param) 

        data = np.array(imgencode)
        stringData = data.tostring()

        queue.put(stringData)

        
        cv2.imshow('image', frame)
            
        key = cv2.waitKey(1)
        if key == 27:
            break


HOST = '{host ip}'           
PORT = 9999

# create socket object
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 

start_new_thread(webcam, (enclosure_queue,)) 

while True: 

    message = '1'
    client_socket.send(message.encode()) #encode 

    client_socket.recv(1024) 

    stringData = enclosure_queue.get()
    client_socket.send(str(len(stringData)).ljust(16).encode()) 
    client_socket.send(stringData)                      


client_socket.close() 