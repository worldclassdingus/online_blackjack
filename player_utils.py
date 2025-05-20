import random
from player import Gambler

# Utility functions for the game

def create_players(n):
	"""Creates a list of Gambler instances: n-1 AI players, 1 main player, and 1 dealer."""
	players = [Gambler('ai') for _ in range(n - 1)]
	players.append(Gambler('main'))  # Add the main player
	random.shuffle(players)          # Shuffle player order
	players.append(Gambler('dealer'))  # Add dealer at the end
	return players

def draw_cards(players, deck):
	"""Deals cards to each player. Dealer gets 1, others get 2."""
	for player in players:
		num_cards = 1 if player.role == 'dealer' else 2
		player.draw(deck.deal(num_cards))

def update_all_values(players):
	"""Updates the value for each player."""
	for player in players:
		player.update_value()

def print_all_cards(players):
	"""Prints the cards and values for each player with role-based formatting."""
	for player in players:
		if player.role == 'dealer':
			print(f'dealer: {player.print_cards()}??')
		elif player.role == 'main':
			print(f'you: {player.print_cards()}[{player.value}]')
		else:
			print(f'ai: {player.print_cards()}[{player.value}]')

def hit(player, deck):
	"""Handles a hit action for a player, including drawing and displaying the card."""
	card = deck.deal(1)
	print(*card)
	player.draw(card)
	player.update_value()
	print(f'{player.print_cards()}[{player.value}]')

def print_result(players):
	"""Prints the result (win, lose, push, bust) for each non-dealer player."""
	dealer = players[-1]
	dealer_value = dealer.value

	for player in players:
		if player.role == 'dealer':
			continue

		print(f'{player.print_cards()}[{player.value}] - ', end='')

		if player.value > 21:
			print('bust')
		elif dealer_value > 21 or player.value > dealer_value:
			print('win')
		elif player.value == dealer_value:
			print('push')
		else:
			print('lose')
