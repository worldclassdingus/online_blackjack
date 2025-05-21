import threading
import select

import server_utils

# handles connecting to a game
# has client logic


# main function
def connect():
    host = input('enter public ip address of the server (local ip if on LAN): ')
    port = input('enter port number: ')

    username = input('enter username: ')

    global client
    client = server_utils.create_client(host, port, username)

    print('waiting for game to start')

    # print messages from server
    receive_thread = threading.Thread(target = receive, daemon = True)
    receive_thread.start()


# threading functions

# recieve messages from the server
def receive():
    while True:
        readable, _, _ = select.select([client], [], [], 1)
        if readable:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)