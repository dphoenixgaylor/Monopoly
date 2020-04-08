from dependencies import *
import gameplay_functions as GF

player = players[player_number]
    
if(same_turn == False):
    print(colored("\nIt's your turn, {}!".format(player.name), player.color))
    same_turn = True
    
print(colored("\nPress enter to roll. Type [?] for other options.", player.color))

response = input()

if(response == ''):
    player.move_position(other_parameters, space_list, specials)
    
    if(player_number + 1 == len(players)):
        player_number = 0
    else:
        player_number += 1
   
    same_turn = False
    turn_counter += 1
    
    player.landing(specials, chance_cards, community_cards, chance_deck, community_deck)
    
elif(response == '?'): GF.controls(player)
elif(response.lower() == 'me'): GF.me(player, space_list = space_list)
elif(response.upper() == 'T'): GF.trade(player, players = players)
elif(response.upper() == 'B'): GF.board(players = players, properties = properties, railroads = railroads, utilities = utilities, 
                                        space_list = space_list)
elif(response.upper() == 'O'): GF.overview(player)
elif(response.upper() == 'P'): GF.view_properties(player, properties = properties, property_names = property_names, other_params = other_parameters)
elif(response.upper() == 'C'): GF.change_color(player)
elif(response.upper() == 'S'): 
    quit = False
    autosave = False
    exec(open("scripts\\save_game.py").read())
elif(response.lower() == 'quit'): 
    quit = True
    autosave = False
    exec(open("scripts\\save_game.py").read())
    
else:
    print(colored("The option you have picked doesn't exist. Please try again!", "yellow"))
    exec(open("scripts\\player_turn.py").read())

autosave = True
quit = False

exec(open("scripts\\save_game.py").read())    
exec(open("scripts\\player_turn.py").read())