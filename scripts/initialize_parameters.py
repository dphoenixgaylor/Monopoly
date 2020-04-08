from dependencies import *
import initializing_functions as IF

game_type, dev = IF.new_or_return()


if(game_type == 'returning'):
    exec(open("scripts\\retrieve_parameters.py").read())
    sys.exit()

if(game_type == 'new'):
    exec(open("scripts\\new_game.py").read())
    sys.exit()
       
       
print("What is the name of your board setup file?")
_input = input()
file = 'board_setup/' + _input
print("\nChecking '{}'...\n".format(file))
    
try:
    properties, property_names, property_locations = IF.load_properties(file)
    railroads, railroad_names, railroad_locations = IF.load_railroads(file)
    utilities, utility_names, utility_locations = IF.load_utilities(file)
    specials, special_names, special_locations = IF.load_specials(file)

    chance_deck, community_deck = IF.load_decks(file)
    deck_lengths = len(chance_deck), len(community_deck)
    chance_cards = IF.first_shuffle_chance_cards(deck_lengths[0])
    community_cards = IF.first_shuffle_community_cards(deck_lengths[1])
    
    other_parameters = IF.load_other_parameters(file)

    free_parking = 0
    
except FileNotFoundError:
    print(colored("The board setup file you have tried to load does not exist. Please check for correctness and try again.", "red"))
    print(colored("Going back to main menu...\n", "red"))
    exec(open("scripts\\initialize_parameters.py").read())

else:
    exec(open("scripts\\generate_spaces.py").read())