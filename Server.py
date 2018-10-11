import socket
host = ''
port = 3333
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((host, port))
serv.listen(1)
clien, addr = serv.accept()
while True:
    data = clien.recv(16).decode('utf-8').strip()
    if not data:
        break
    if data == 'Close':
        clien.close()
        break
    sz = int(data.strip())
    img = b''
    while sz > len(img):
        img += clien.recv(1024)
    out = open('result_filename.jpg', 'wb')
    out.write(img)
    out.close()
    clien.send("Done".encode('utf-8'))
serv.close()

