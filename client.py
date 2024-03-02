# this is the client code

import socket, cv2, pickle, struct
import pyshine as ps
import imutils

camera = False

if camera == True:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture("D:\Academics\Research\Holistic\SocketProgramming\data\Stop_motion1.mp4")

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# host_ip = '10.211.55.18' #change this (see the description)
host_ip = '192.168.56.1' #change this (see the description)

port = 9999
client_socket.connect((host_ip,port))

if client_socket:
    while(vid.isOpened()):
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame,width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a)) + a
            client_socket.sendall(message)
            # cv2.imshow(f"TO: {host_ip}",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
        except:
            print('Video finished!')
            break 

