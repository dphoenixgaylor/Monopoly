from dependencies import *
from monopoly_classes import *
import initializing_functions as IF
import gameplay_functions as GF


file = 'board_setup/standard_setup.xlsx'
dev = False

try:
    print("Loading properties...")
    properties, property_names, property_locations = IF.load_properties(file)
    railroads, railroad_names, railroad_locations = IF.load_railroads(file)
    utilities, utility_names, utility_locations = IF.load_utilities(file)
    time.sleep(0.3)
    
    print("Assembling the board...")
    specials, special_names, special_locations = IF.load_specials(file)
    time.sleep(0.3)
    
    print("Shuffling the chance and community chest cards...")
    chance_deck, community_deck = IF.load_decks(file)
    deck_lengths = len(chance_deck), len(community_deck)
    chance_cards = IF.first_shuffle_chance_cards(deck_lengths[0])
    community_cards = IF.first_shuffle_community_cards(deck_lengths[1])
    time.sleep(0.3)
    
    other_parameters = IF.load_other_parameters(file)
    free_parking = 0
    
    print(colored("Done!\n", "green"))
    
except FileNotFoundError:
    print(colored("The default setup file was not found. Please move it back to board_setup or redownload the program.", "red"))
    sys.exit()

exec(open("scripts\\generate_spaces.py").read())
    
players = IF.create_players(other_parameters)
player_number = 0
turn_counter = 0

same_turn = False
exec(open("scripts\\player_turn.py").read())