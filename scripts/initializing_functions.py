from dependencies import *
from monopoly_classes import *

        
def new_or_return():
    print("Are you starting a new game or returning to an existing game? Type 'N' for new game or 'R' for returning!")
    time.sleep(0.3)
    _input = input("N/R: ").lower()
    is_quit(_input)
    print('\n')

    fails = 0

    while(_input not in ['n', 'r', 'dev', 'quit']):
        fails += 1
        
        if(fails > 2):
            print(colored("Too many failed attempts... exiting.", "red"))
            sys.exit()
            
        print(colored("Please type either 'N' for a new game or 'R' if you're returning.", "yellow"))
        print(colored("Alternatively, type 'quit' to exit the game or 'dev' to access developer tools.", "yellow"))
        _input = input("N/R: ").lower()
        is_quit(_input)
        print('\n')

    if(_input == 'n'):
        print(colored("New game!\n", "magenta"))
        time.sleep(0.3) 
        return ('new', False)
        
    elif(_input == 'r'):
        print(colored("Returning game!\n", "green"))
        time.sleep(0.3) 
        return ('returning', False)
        
    elif(_input == 'dev'):
        print(colored("DEVELOPER\n", "blue"))
        time.sleep(0.3)
        return ('dev', True)
            

def load_properties(filename):
    properties_raw = pd.read_excel(filename, sheet_name = 'properties')
    properties = {}

    for p in range(len(properties_raw)):
        p_name = properties_raw.loc[p]['Name'].title()
        p_details = Property(p_name,
                             properties_raw.loc[p]['Location'], 
                             properties_raw.loc[p]['Color'].lower(),
                             properties_raw.loc[p]['Rents'].split(";"),
                             properties_raw.loc[p]['Prices'].split(";"))
        
        properties[p_name] = p_details
    
    property_names = properties_raw['Name'].values.astype(str)
    property_names = [property_names[i].title() for i in range(len(property_names))]
    
    property_locations = properties_raw['Location'].values
    
    return properties, property_names, property_locations

    
def load_railroads(filename):
    railroads_raw = pd.read_excel(filename, sheet_name = 'railroads')
    railroads = {}

    for r in range(len(railroads_raw)):
        r_name = railroads_raw.loc[r]['Name'].title()
        r_details = Railroad(r_name,
                             railroads_raw.loc[r]['Location'], 
                             railroads_raw.loc[r]['Rents'].split(";"),
                             railroads_raw.loc[r]['Prices'])
        
        railroads[r_name] = r_details
    
    railroad_names = railroads_raw['Name'].values.astype(str)
    railroad_names = [railroad_names[i].title() for i in range(len(railroad_names))]
    
    railroad_locations = railroads_raw['Location'].values
    
    return railroads, railroad_names, railroad_locations
    
    
def load_utilities(filename):
    utilities_raw = pd.read_excel(filename, sheet_name = 'utilities')
    utilities = {}

    for u in range(len(utilities_raw)):
        u_name = utilities_raw.loc[u]['Name'].title()
        u_details = Utility(u_name,
                            utilities_raw.loc[u]['Location'], 
                            utilities_raw.loc[u]['RentMult'].split(";"),
                            utilities_raw.loc[u]['Prices'])
        
        utilities[u_name] = u_details
    
    utilities_names = utilities_raw['Name'].values.astype(str)
    utilities_names = [utilities_names[i].title() for i in range(len(utilities_names))]
    
    utilities_locations = utilities_raw['Location'].values
    
    return utilities, utilities_names, utilities_locations
    

def load_specials(filename):
    specials = pd.read_excel(filename, sheet_name = "special_locations").dropna(subset = ['Location'])
    
    special_names = specials['Name'].values.astype(str)
    special_names = [i for i in special_names]
    
    special_locations = specials['Location'].values
    
    return specials, special_names, special_locations
    


def load_decks(filename):
    chance_deck = pd.read_excel(filename, sheet_name = 'chance_cards')
    community_deck = pd.read_excel(filename, sheet_name = 'community_cards')
    
    return chance_deck, community_deck
    
    
def first_shuffle_chance_cards(deck_length):
    cards = list(range(deck_length))
    cards = random.sample(cards, deck_length)
    
    return cards


def first_shuffle_community_cards(deck_length):
    cards = list(range(deck_length))
    cards = random.sample(cards, deck_length)
    
    return cards


def load_other_parameters(filename):
    other_params_raw = pd.read_excel('board_setup\\standard_setup.xlsx', sheet_name = 'other_parameters')[['Parameter', 'Value']]
    other_params_tup = [(other_params_raw['Parameter'][i], other_params_raw['Value'][i]) for i in range(len(other_params_raw))]
    other_params = dict(other_params_tup)
    other_params['dice_sizes'] = list(map(int, other_params['dice_sizes'][1:-1].split(",")))
    
    return other_params
    
    
def create_players(other_params):
    players = []
    
    print("Press enter to start or type 'quit' at any time to quit!")
    _input = input()
    is_quit(_input)
    
    print("How many players will there be today?")
    
    fails = 0
    
    while(True):
        try:
            numPlayers = input('Number of Players: ')
            is_quit(numPlayers)
            numPlayers = int(numPlayers)
            assert numPlayers > 0
            break
        
        except ValueError:
            if(fails > 2):
                print(colored("\nToo many failed attempts... exiting.", "red"))
                sys.exit()
        
            print(colored("\nPlease type in a number.", "yellow"))
            fails += 1
        
        except AssertionError:
            if(fails > 2):
                print(colored("\nToo many failed attempts... exiting.", "red"))
                sys.exit()
            
            print(colored("\nPlease type in a positive number.", "yellow"))
            fails += 1
                
    if(numPlayers == 1):
        print(colored("Please note that Monopoly is best played with more than 1 player.", "blue"))
        
    print('\n')
    print('For each player, please give your name and favorite color.')
    print("Available colors include: '{}', '{}', '{}', '{}', '{}', '{}', and '{}'.".format(colored("grey", "grey"), \
            colored("red", "red"), colored("green", "green"), colored("yellow", "yellow"), colored("blue", "blue"), \
            colored("magenta", "magenta"), colored("cyan", "cyan")))
    
    for p in range(numPlayers):
        n = input("Player {}'s name: ".format(p+1)).lower().capitalize()
        is_quit(n)
        c = input("Player {}'s favorite color: ".format(p+1)).lower()
        is_quit(c)
        
        fails = 0
        while(c not in ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan']):
            fails += 1
            if(fails > 2):
                print(colored("Too many failed attempts... picking grey.", "red"))
                c = 'grey'
                break
            print(colored('Please choose from the following colors: "grey", "red", "green", yellow", "blue", "magenta", "cyan".', "yellow"))
            c = input("Player {}'s favorite color: ".format(p+1)).lower()
            is_quit(c)
            
        print('\n')
        
        players.append(Player(n, c, other_params))
        
    print("Great!\n\nGood luck to the players...")
    for p in players:
        print(colored(p.name, p.color))
        
    return players
    
    
def is_quit(var):
    if(var.lower() == 'quit'):
        print(colored("\nExiting... see you next time!", "green"))
        sys.exit()