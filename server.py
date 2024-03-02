import socket, cv2, pickle, struct
import imutils
import threading
import pyshine as ps


server_socket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

def show_client(addr,client_socket):
    try:
        print('client {} connected'.format(addr))
        if client_socket:
                data =b""
                payload_size = struct.calcsize("Q")
                while True:
                     while len(data)<payload_size:
                          packet = client_socket.recv(4*1024) #4K
                          if not packet: break
                          data +=packet
                     packed_msg_size = data[:payload_size]
                     data = data[payload_size:]
                     msg_size = struct.unpack("Q",packed_msg_size)[0]

                     while len(data)<msg_size:
                          data += client_socket.recv(4*1024)
                     frame_data = data[:msg_size]
                     data = data[msg_size:]
                     frame =pickle.loads(frame_data)
                     text = f"CLIent: {addr}"
                     frame = ps.putBText(frame,text,10,10,vspace=10,hspace=1, font_scale=0.7,background_RGB=(255,0,0),text_RGB=(255,250,250))
                     cv2.imshow(f"FROM{addr}",frame)
                     key = cv2.waitKey(1) & 0xFF
                     if key == ord('q'):
                          break
    except Exception as e:
         print(f"CLIENT {addr} DISCONNECTED")
         pass
    
while True:
    client_socket,addr = server_socket.accept()
    thread = threading.Thread(target=show_client,args=(addr,client_socket))
    thread.start()
    print("TOTAL_CLIENTS ",threading.activeCount()-1)



