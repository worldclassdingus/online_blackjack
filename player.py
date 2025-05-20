
# master gambler class
# stores cards and a value
class Gambler:
    def __init__(self, role):
        self.cards = []
        self.value = 0

        # role variable determines whether the player is the actual player, the dealer, or ai
        self.role = role
    
    # draw cards
    # takes a list of Cards (instances of the Card class) and adds it self.cards
    def draw(self, cards):
        self.cards += cards
    
    # updates self.value for new cards
    def update_value(self):
        self.value = 0

        for card in self.cards:
            self.value += card.value
        
        # check for aces
        # aces are 1 to start, but if the value is 11 or less it becomes 11
        for card in self.cards:

            if card.rank == 'A' and self.value <= 11:
                self.value += 10
    
    # cleanly print cards
    # returns a string
    def print_cards(self):
        card_list = ''

        for card in self.cards:
            card_list += f'{card} '
        
        return card_list


# real player class
# stores a username and the address it is connected to
# stores its communication socket(the one the server uses to talk to it)
class Player(Gambler):
    def __init__(self, role, socket, address, username):
        super().__init__(role)
        self.socket = socket
        self.address = address
        self.username = username