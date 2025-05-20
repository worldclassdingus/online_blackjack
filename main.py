import random
import time

from deck import Deck
from player import Gambler
from player import Player
import player_utils
import server_utils

# main file that runs the game loop

print("Welcome to the casino!\nType 'host' to host a server\nType 'connect' to connect to a server\nHit enter to play singleplayer")
choice = input('')

# hosting a server
# host end of the game
if choice == 'host':
    host = input('enter your local ip address: ')
    port = input('enter port number: ')
    server = server_utils.create_server(host, port)

    players = []
    waiting = True

    server.listen(7)

    # accept player connections and add them to the list of players
    while len(players) <= 7:
        print('waiting for players...')

        player_socket, player_address = server.accept()
        print(f'new connection: {player_address}')

        # send the join message to all players
        player_username = player_socket.recv(1024).decode('utf-8')
        print(f'{player_username} joined')
        server_utils.send_all(f'{player_username} joined', players)

        players.append(Player('player', player_socket, player_address, player_username))

        # after each connection, ask the host if they want to start the game
        print('players: ', end = '')
        for player in players:
            print(f'{player.username} ')
        start = input(f'start game? (y/n) ')
        if start == 'y':
            break
    
    # start the game
    print('game started')
    server_utils.send_all('game started', players)
    
    deck = Deck()
    dealer = Gambler('dealer')

    player_utils.draw_cards(players, deck)

# connect to a server
# player end of the game
elif choice == 'connect':
    host = input('enter public ip address of the server (local ip if on LAN): ')
    port = input('enter port number: ')

    client = server_utils.create_client(host, port)

    username = input('enter username: ')
    client.send(username.encode('utf-8'))

    # wait for game to start
    print('waiting for game to start')
    while True:
        message = client.recv(1024).decode('utf-8')
        if message:
            print(message)

        if message == 'game started':
            break



# number of players (not including dealer)
player_count = 7


# create the deck
deck = Deck()

# create players, draw cards, and update values  
players = player_utils.create_players(player_count)
player_utils.draw_cards(players, deck)
player_utils.update_all_values(players)

# print everyone's cards
player_utils.print_all_cards(players)


# main game loop


# the dealer's value
dealer_value = 0

# loop through all players
for player in players:

    # dealer decisions
    if player.role == 'dealer':

        # print message saying it's the dealer's turn
        print("---DEALER'S TURN---")
        player.draw(deck.deal(1))
        player.update_value()
        print(f'{player.print_cards()}[{player.value}]')

        # continue hitting until 17
        while player.value < 17:
            time.sleep(1)
            player_utils.hit(player, deck)

        # print what the dealer got
        if player.value <= 21:
            print(f'dealer: {player.value}')
        else:
            print(f'dealer busted')

    # regular decisions
    else:
        # print info
        print('---YOUR TURN---')
        print(f'{player.print_cards()}[{player.value}]')

        # keep making decisions until 21 or bust
        while player.value < 21:

            choice = input('hit or stay? ')

            # if the choice is stay, break the loop. If the choice is hit, hit and stay in the loop
            if choice == 'stay':
                break
            elif choice == 'hit':
                player_utils.hit(player, deck)

            # double down
            # get one more card and break the loop
            elif choice == 'double down':
                player_utils.hit(player, deck)
                break
            
            # print everyone's cards again
            elif choice == 'info':
                player_utils.print_all_cards(players)
        
        # after the loop breaks, the player will either have stood, busted, or hit blackjack
        # print a message saying which one
        if player.value < 21:
            print(f'you stood at {player.value}')
        elif player.value == 21:
            print('blackjack!')
        else:
                print('you busted :(')
        
        time.sleep(1)

time.sleep(1)

# print results
player_utils.print_result(players)