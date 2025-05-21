import connector
import host

# main file that runs everything
# multiplayer code is stored in host.py and connector.py
# singleplayer code is in here

print("Welcome to the casino!\nType 'host' to host a server\nType 'connect' to connect to a server\nHit enter to play singleplayer")
choice = input('')

# hosting a server
# host end of the game
if choice == 'host':
    host.host()

# connect to a server
# player end of the game
elif choice == 'connect':
    connector.connect()



# # number of players (not including dealer)
# player_count = 7


# # create the deck
# deck = Deck()

# # create players, draw cards, and update values  
# players = player_utils.create_players(player_count)
# player_utils.draw_cards(players, deck)
# player_utils.update_all_values(players)

# # print everyone's cards
# player_utils.print_all_cards(players)


# main game loop


# the dealer's value
# dealer_value = 0

# # loop through all players
# for player in players:

#     # dealer decisions
#     if player.role == 'dealer':

#         # print message saying it's the dealer's turn
#         print("---DEALER'S TURN---")
#         player.draw(deck.deal(1))
#         player.update_value()
#         print(f'{player.print_cards()}[{player.value}]')

#         # continue hitting until 17
#         while player.value < 17:
#             time.sleep(1)
#             player_utils.hit(player, deck)

#         # print what the dealer got
#         if player.value <= 21:
#             print(f'dealer: {player.value}')
#         else:
#             print(f'dealer busted')

#     # regular decisions
#     else:
#         # print info
#         print('---YOUR TURN---')
#         print(f'{player.print_cards()}[{player.value}]')

#         # keep making decisions until 21 or bust
#         while player.value < 21:

#             choice = input('hit or stay? ')

#             # if the choice is stay, break the loop. If the choice is hit, hit and stay in the loop
#             if choice == 'stay':
#                 break
#             elif choice == 'hit':
#                 player_utils.hit(player, deck)

#             # double down
#             # get one more card and break the loop
#             elif choice == 'double down':
#                 player_utils.hit(player, deck)
#                 break
            
#             # print everyone's cards again
#             elif choice == 'info':
#                 player_utils.print_all_cards(players)
        
#         # after the loop breaks, the player will either have stood, busted, or hit blackjack
#         # print a message saying which one
#         if player.value < 21:
#             print(f'you stood at {player.value}')
#         elif player.value == 21:
#             print('blackjack!')
#         else:
#                 print('you busted :(')
        
#         time.sleep(1)

# time.sleep(1)

# # print results
# player_utils.print_result(players)