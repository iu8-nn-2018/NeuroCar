import socket
host = ''
port = 3333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
image = open('filename.jpg', 'rb')
data = image.read()
sock.send('%16d'.encode('utf-8') % len(data))
sock.send(data)
image.close()
res = sock.recv(1024)
print(res.decode('utf-8'))
sock.close()

