from dependencies import *
import retrieving_functions as RF

directory_name = RF.get_directory_name()

if(directory_name == 'saves\\GO BACK'):
    exec(open("scripts\\initialize_parameters.py").read())
    sys.exit()

print("\nRetrieving properties and assembling the board...")
properties, property_names, property_locations = RF.retrieve_properties(directory_name + '\\properties.csv')
railroads, railroad_names, railroad_locations = RF.retrieve_railroads(directory_name + '\\railroads.csv')
utilities, utility_names, utility_locations = RF.retrieve_utilities(directory_name + '\\utilities.csv')
space_list = RF.retrieve_space_list(directory_name + '\\space_list.csv')
time.sleep(0.3)

print("Retrieving players and their attributes...")
players = RF.retrieve_players(directory_name + '\\players.csv')
time.sleep(0.3)

print("Retrieving the chance and community chest cards...")
chance_deck = RF.retrieve_chance_deck(directory_name)
community_deck = RF.retrieve_community_deck(directory_name)
chance_cards = RF.retrieve_chance_cards(directory_name)
community_cards = RF.retrieve_community_cards(directory_name)
time.sleep(0.3)

print("Retrieving the free parking money...")
free_parking = RF.retrieve_free_parking(directory_name)
time.sleep(0.3)

print(colored("\nDone!", "green"))

turn = 0

player = players[turn]
print(colored("\nIt's your turn, {}!".format(player.name), player.color))
exec(open("scripts\\player_turn.py").read())