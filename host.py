import threading
import time
import random

import server_utils
import player_utils
from deck import Deck
from player import Gambler, Player

# handles hosting a game
# has game logic

players = []

# main function
def host():
    global server
    host = input('enter your local ip address: ')
    port = input('enter port number: ')
    server = server_utils.create_server(host, port)

    server.listen(7)

    global waiting
    waiting = True
    print('waiting for players...')

    # threads
    wait_to_start_thread = threading.Thread(target=wait_to_start, daemon=True)
    wait_to_start_thread.start()

    accept_players_thread = threading.Thread(target=accept_players, daemon=True)
    accept_players_thread.start()
    
    # if the max player limit is reached, wait until the host starts the game
    wait_to_start_thread.join()
    random.shuffle(players)
    
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
        server_utils.spec_send_all(f"---{player.username}'s turn---\n{player.print_cards()}", 
                                   f'---YOUR TURN---\n{player.print_cards()}', 
                                   players, player)
        
        while player.value < 21:
            player.socket.send('TURN'.encode('utf-8'))
            choice = player.socket.recv(1024).decode('utf-8')

            if choice == 'hit':
                card = deck.deal(1)
                player.draw(card)
                server_utils.send_all(f'hit: {card[0]}\n{player.print_cards()}', players)
            elif choice == 'stay':
                break
        
        if player.value == 21:
            server_utils.send_all('blackjack!', players)
        elif player.value > 21:
            server_utils.spec_send_all(f'{player.username} busted :(',
                                       f'you busted :(',
                                       players, player)
        else:
            server_utils.spec_send_all(f'{player.username} stood at {player.value}',
                                       f'you stood at {player.value}',
                                       players, player)
        time.sleep(1)
    
    # dealer time
    dealer.draw(deck.deal(1))
    server_utils.send_all(f"---DEALER'S TURN---\n{dealer.print_cards()}[{dealer.value}]", players)
    time.sleep(1)

    while dealer.value < 17:
        card = deck.deal(1)
        dealer.draw(card)
        server_utils.send_all(f'hit: {card[0]}\n{dealer.print_cards()}[{dealer.value}]', players)
        time.sleep(1)

    if dealer.value <= 21:
        server_utils.send_all(f'dealer: {dealer.value}', players)
    else:
        server_utils.send_all(f'dealer busted', players)
    
    # print results
    for player in players:
        result = f'{player.print_cards()} - '

        if player.value > 21:
            result += 'bust'
        elif player.value > dealer.value or dealer.value > 21:
            result += 'win'
        elif player.value == dealer.value:
            result += 'push'
        else:
            result += 'lose'
        
        server_utils.send_all(f'{player.username}: {result}\n', players)

    server_utils.send_all('END')



# threading functions

# wait for players and accept player connections
def accept_players():
    global players
    global waiting
    while True: 
        player_socket, player_address = server.accept()
        print(f'new connection: {player_address}')

        if waiting:
            # accept player connections and add them to the list of players

            # get username and add player to the list
            player_socket.send('USERNAME'.encode('utf-8'))
            player_username = player_socket.recv(1024).decode('utf-8')
            players.append(Player('player', player_socket, player_address, player_username))

            # send the join message to all players
            print(f'{player_username} joined')
            server_utils.send_all(f'{player_username} joined', players)

            # send the new player the list of players
            player_list = ''
            for player in players:
                player_list += f'{player.username} '
            player_socket.send(f'players: {player_list}'.encode('utf-8'))
        else:
            player_socket.send('game has already started'.encode('utf-8'))
            player_socket.close()
            print(f'connection with {player_address} denied: game already started')
            break

        # stop waiting if 7 players join
        if len(players) >= 7:
            print('maximum player count reached')
            waiting = False
            break


# let the host choose when to start the game
def wait_to_start():
    global waiting

    while True:
        start = input('')
        if start == 'start':
            waiting = False
            break