import random
import time

from deck import Deck
from player import Gambler, Player
import player_utils
import server_utils

# Main game loop

print("Welcome to the casino!")
print("Type 'host' to host a server")
print("Type 'connect' to connect to a server")
print("Hit enter to play singleplayer")

choice = input('').strip().lower()

# Multiplayer setup
players = []

# Hosting a server
if choice == 'host':
	host = input('Enter your local IP address: ').strip()
	port = int(input('Enter port number: ').strip())
	server = server_utils.create_server(host, port)

	server.listen(7)
	print("Waiting for players to join...")

	while len(players) < 7:
		player_socket, player_address = server.accept()
		print(f'New connection: {player_address}')

		player_username = player_socket.recv(1024).decode('utf-8')
		players.append(Player('player', player_socket, player_address, player_username))
		print(f'{player_username} joined')

		print('Current players:', ', '.join(p.username for p in players))

		start = input('Start game? (yes/no): ').strip().lower()
		if start == 'yes':
			break

	print('Game started.')

# Connecting to a server
elif choice == 'connect':
	host = input('Enter the IP address of the server: ').strip()
	port = int(input('Enter port number: ').strip())

	client = server_utils.create_client(host, port)

	username = input('Enter username: ')
	client.send(username.encode('utf-8'))

	print('Waiting for the host to start the game...')
	# Here, you'd need to implement client sync logic
	exit()  # Prevents singleplayer code from running under client mode

# Singleplayer setup
if choice == '':
	player_count = 7  # Not including dealer
	players = player_utils.create_players(player_count)

	# Create and shuffle deck
	deck = Deck()

	# Deal cards and update values
	player_utils.draw_cards(players, deck)
	player_utils.update_all_values(players)

	# Print everyone's cards
	player_utils.print_all_cards(players)

	# --- Game Loop ---
	for player in players:

		if player.role == 'dealer':
			print("\n--- DEALER'S TURN ---")
			player.draw(deck.deal(1))
			player.update_value()
			print(f'{player.print_cards()}[{player.value}]')

			while player.value < 17:
				time.sleep(1)
				player_utils.hit(player, deck)

			if player.value <= 21:
				print(f'Dealer stands at {player.value}')
			else:
				print('Dealer busted.')

		else:
			print("\n--- YOUR TURN ---")
			print(f'{player.print_cards()}[{player.value}]')

			while player.value < 21:
				action = input('Choose: hit / stay / double down / info\n> ').strip().lower()

				if action == 'stay':
					break
				elif action == 'hit':
					player_utils.hit(player, deck)
				elif action == 'double down':
					player_utils.hit(player, deck)
					break
				elif action == 'info':
					player_utils.print_all_cards(players)
				else:
					print("Invalid input. Try again.")

			if player.value < 21:
				print(f'You stood at {player.value}')
			elif player.value == 21:
				print('Blackjack!')
			else:
				print('You busted :(')

			time.sleep(1)

	time.sleep(1)
	player_utils.print_result(players)