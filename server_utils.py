import socket

# file that handles the multiplayer and server creation

# create server
def create_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, int(port)))

    return server

# create client
def create_client(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, int(port)))

    return client

# send a message to all players
def send_all(message, players):
    for player in players:
        player.socket.send(message.encode('utf-8'))

# send a message to all players, but with a different message for one player
def spec_send_all(message, spec_message, players, spec_player):
    for player in players:
        if player is spec_player:
            player.socket.send(spec_message.encode('utf-8'))
        else:
            player.socket.send(message.encode('utf-8'))