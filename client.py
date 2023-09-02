import socket

host = '127.0.0.1'
port = 9000
buffer_size = 20  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)
while 1:
    data = conn.recv(buffer_size)
if not data: 
    pass
print("received data:", data)
conn.send(data)  # echo
conn.close()