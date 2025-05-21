import threading
import select
import time

import server_utils
import player_utils
from deck import Deck
from player import Gambler, Player

# handles hosting a game
# has game logic

# global variables (for threading)
waiting = True
players = []

def host():
    host = input('enter your local ip address: ')
    port = input('enter port number: ')
    server = server_utils.create_server(host, port)

    server.listen(7)
    print('waiting for players...')

    # threads
    wait_to_start_thread = threading.Thread(target = wait_to_start, daemon = True)
    wait_for_players_thread = threading.Thread(target = wait_for_players, args = (server,), daemon = True)

    wait_to_start_thread.start()
    wait_for_players_thread.start()
    
    # if the max player limit is reached, wait until the host starts the game
    wait_for_players_thread.join()
    wait_to_start_thread.join()
    
    # start the game
    print('game started')
    server_utils.send_all('game started', players)
    time.sleep(2)
    
    # actual game loop
    deck = Deck()
    dealer = Gambler('dealer')

    # print everyone's cards
    player_utils.draw_cards(players, deck)
    dealer.draw(deck.deal(1))
    message = f'{player_utils.print_all_cards(players)}dealer: {dealer.print_cards()}??'
    server_utils.send_all(message, players)
    time.sleep(5)

    # loop through everyone
    for player in players:
        server_utils.spec_send_all(f"{player.username}'s turn", '---YOUR TURN---\n', players, player)
        server_utils.send_all(f'{player.print_cards()}[{player.value}]\n', players)




# threading functions

# wait for players and accept player connections
def wait_for_players(server):
    global players
    global waiting
    while waiting:
        readable, _, _ = select.select([server], [], [], 1)

        # accept player connections and add them to the list of players
        if readable:
            player_socket, player_address = server.accept()
            print(f'new connection: {player_address}')

            # send the new player the list of players that joined before they did
            if players:
                player_list = ''
                for player in players:
                    player_list += f'{player.username} '
                player_socket.send(f'players: {player_list}'.encode('utf-8'))

            # send the join message to all players
            player_username = player_socket.recv(1024).decode('utf-8')
            print(f'{player_username} joined')
            server_utils.send_all(f'{player_username} joined', players)

            players.append(Player('player', player_socket, player_address, player_username))

        # stop waiting if 7 players join
        if len(players) >= 7:
            waiting = False
            print('maximum player count reached')


# let the host choose when to start the game
def wait_to_start():
    global waiting

    while True:
        start = input()
        print(start)
        if start == 'start':
            waiting = False
            break