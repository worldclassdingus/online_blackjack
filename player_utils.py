import random
from player import Gambler

# utility functions file


# create players
# returns a list of Player classes
def create_players(n):
    players = []

    # create player_count - 1 ai players
    for i in range(n - 1):
        players.append(Gambler('ai'))

    # create main player
    players.append(Gambler('main'))

    # randomize player order
    random.shuffle(players)

    # add dealer at the end of the list
    players.append(Gambler('dealer'))

    return players

# draw cards for everyone
def draw_cards(players, deck):
    for player in players:
        player.draw(deck.deal(2))


# update values for all players
def update_all_values(players):
    for player in players:
        player.update_value()

# print everyone's cards and values
def print_all_cards(players):
    cards_to_print = ''
    for player in players:

        # different prints for dealer, player, and ai
        if player.role == 'dealer':
            cards_to_print += f'dealer: {player.print_cards()}\n'
        elif player.role == 'player':
            cards_to_print += f'{player.username}: {player.print_cards()}\n'
        else:
            cards_to_print += f'ai: {player.print_cards()}\n'
    
    return cards_to_print

# function for hitting
def hit(player, deck):

    # draw the top card of the deck by itself to print it
    card = deck.deal(1)
    print(*card)

    # draw the card, and print the new cards and value
    player.draw(card)
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
