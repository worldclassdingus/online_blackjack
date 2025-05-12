import random
from player import Player

# utility functions file


# create players
# returns a list of Player classes
def create_players(n):
    players = []

    # create player_count - 1 ai players
    for i in range(n - 1):
        players.append(Player('ai'))

    # create main player
    players.append(Player('main'))

    # randomize player order
    random.shuffle(players)

    # add dealer at the end of the list
    players.append(Player('dealer'))

    return players

# draw cards for everyone
# takes the list of players (including the dealer) and the deck
def draw_cards(players, deck):
    for player in players:

        # if the player is the dealer, draw 1. Otherwise draw 2
        if player.role == 'dealer':
            player.draw(deck.deal(1))
        else:
            player.draw(deck.deal(2))

# update values for all players
def update_all_values(players):
    for player in players:
        player.update_value()

# print everyone's cards and values
def print_all_cards(players):
    for player in players:

        # different prints for dealer, player, and ai
        if player.role == 'dealer':
            print(f'dealer: {player.print_cards()}??')
        elif player.role == 'main':
            print(f'you: {player.print_cards()}[{player.value}]')
        else:
            print(f'ai: {player.print_cards()}[{player.value}]')

# function for hitting
def hit(player, deck):

    # print the card they draw (the top card of the deck) before it is removed from the deck
    print(f'{deck.cards[len(deck.cards) - 1]}')

    # draw the card, update the value, and print the new cards and value
    player.draw(deck.deal(1))
    player.update_value()
    print(f'{player.print_cards()}[{player.value}]')

# print who won, lost, or busted at the end
# takes the list of players (dealer needs to be at the end)
def print_result(players):
        
    dealer_value = players[len(players) - 1].value

    for player in players:

        if player.role != 'dealer':
            print(f'{player.print_cards()}[{player.value}] - ', end = '')

            if player.value > 21:
                print('bust')
            elif player.value > dealer_value or dealer_value > 21:
                print('win')
            elif player.value == dealer_value:
                print('push')
            else:
                print('lose')
