import threading
import select

import server_utils

# handles connecting to a game
# has client logic

# global variables(for threading)
game_active = True

def connect():
    host = input('enter public ip address of the server (local ip if on LAN): ')
    port = input('enter port number: ')

    username = input('enter username: ')
    client = server_utils.create_client(host, port, username)

    # wait for game to start
    print('waiting for game to start')
    while True:
        message = client.recv(1024).decode('utf-8')
        if message:
            print(message)

        if message == 'game started':
            break