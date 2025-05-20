# Master gambler class
# Stores cards and a total value
class Gambler:
	def __init__(self, role):
		self.cards = []
		self.value = 0
		self.role = role  # 'main', 'dealer', or 'ai'

	def draw(self, cards):
		"""Adds a list of Card instances to this player's hand."""
		self.cards += cards

	def update_value(self):
		"""Recalculates the total hand value, accounting for Aces."""
		self.value = sum(card.value for card in self.cards)

		# Upgrade one or more Aces from 1 to 11 if it won't bust the hand
		# Each Ace adds +10 more if total <= 11
		for card in self.cards:
			if card.rank == 'A' and self.value <= 11:
				self.value += 10

	def print_cards(self):
		"""Returns a string representation of the player's hand."""
		return ' '.join(str(card) for card in self.cards)


# Real player class for network play
# Stores socket info and username
class Player(Gambler):
	def __init__(self, role, socket, address, username):
		super().__init__(role)
		self.socket = socket
		self.address = address
		self.username = username
