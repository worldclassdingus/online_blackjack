import threading

import server_utils

# handles connecting to a game
# has client logic


# main function
def connect():
    host = input('enter public ip address of the server (local ip if on LAN): ')
    port = input('enter port number: ')

    global username
    username = input('enter username: ')

    global client
    client = server_utils.create_client(host, port)

    # print messages from server
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                if message == 'USERNAME':
                    client.send(username.encode('utf-8'))
                elif message == 'END':
                    print('break')
                elif message == 'TURN':
                    while True:
                        choice = input('')
                        if choice in ('hit', 'stay'):
                            client.send(choice.encode('utf-8'))
                            break
                else:
                    print(message)
        except:
            print('an error occured')
            break

                