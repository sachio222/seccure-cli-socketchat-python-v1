"""SOCKETCHAT by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with client.py and chat via the cli.
-+- Works out of the box with Python3. No libraries needed.
"""

import os
import sys
import socket
from threading import Thread

BUFFSIZE = 4096  # Upped for encryption
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class Chime:
    # Ring my bell, ring my bell
    def __init__(self):
        self.muted = False

    def play(self):
        if not self.muted:
            sys.stdout.write("\a")
        else:
            return


def welcome_msg():

    # Sned @user handle
    while True:
        handle = input("Enter your handle:\n@")
        if handle:
            break
    client.send(handle.encode())

    # Get message from server
    from_server = client.recv(BUFFSIZE)
    print(f"\x1b[4;32;40m{from_server.decode()}\x1b[0m")


def receive():
    # Incoming broadcasts!!
    while True:
        try:
            incoming = client.recv(BUFFSIZE)
            incoming = incoming.decode()

            # Clear line when new text comes in (otherwise it'll glitch out.)
            sys.stdout.write(ERASE_LINE)

            # Display with some sort of colors
            print(f"\r\x1b[1;33;40m{incoming}\x1b[0m")

            # Bell
            chime.play()

        except OSError:
            break


def send(msg=''):
    # Outgoing!!
    while msg != 'exit()':
        if msg == 'mute()':
            chime.muted = True
        elif msg == 'unmute()':
            chime.muted = False
        
        msg = input('')
        client.send(msg.encode())

    # Close on exit()
    client.close()
    print('Disconnected.')
    exit()


# Instantiate sound
chime = Chime()

if __name__ == '__main__':

    host = input('-+- Enter hostname of server: ')
    if not host:
        # Set default
        host = 'ubuntu'

    port = input('-+- Choose port: ')
    if not port:
        # Set default
        port = 12222
    else:
        port = int(port)

    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))  # Opens socket connect if server running.
    except:
        client.connect((host, port))  # For debug

    welcome_msg()

    # Start send/receive threads
    receive_thread = Thread(target=receive)
    receive_thread.start()
    send_thread = Thread(target=send)
    send_thread.start()
