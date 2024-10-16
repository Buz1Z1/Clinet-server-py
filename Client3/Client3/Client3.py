import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(
    ("127.0.0.1", 1234)
)

data = client.recv(1024)
print(data.decode('utf-8'))

auth = False
while auth is False:
    auth = input()
    if auth == "exit":
        break
    client.send(auth.encode('utf-8'))
    d = client.recv(1024)
    d = d.decode('utf-8')
    print(d)
    if d == "Вы авторизованы":
        auth = True
    else:
        auth = False

if auth is True:
    while True:
        msg = input()
        if msg == "exit":
            client.send(msg.encode('utf-8'))
            break
        client.send(msg.encode('utf-8'))
        result = client.recv(1024)
        print(result.decode('utf-8'))

client.close()

