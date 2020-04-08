from dependencies import *
from monopoly_classes import *


def get_directory_name():
    save_list = ['GO BACK'] + list(os.listdir('saves'))
    saved_games = [['GO BACK', '', '']]

    for save_dir in range(1, len(save_list)):
        saved_game = []
        
        date_time = save_list[save_dir].split('_')[0]
        date_time = datetime.strptime(date_time, '%Y%m%d-%H%M') 
        
        saved_game.append(save_list[save_dir].split('_')[1])
        saved_game.append(date_time.strftime('%B %d %Y'))
        saved_game.append(date_time.strftime('%H:%M'))
        
        saved_games.append(saved_game)
        
    print(pd.DataFrame(saved_games, columns = ['Name', 'Date', 'Time']))
    print("\nPlease type the number on the left corresponding to the game you would like to load.")
    print("To delete a game, type in '-' followed by the number.")

    fails = 0
        
    while(True):
        try:
            game = int(input('# '))
            assert (game > -len(save_list)) and (game < len(save_list))
            break

        except ValueError:
            if(fails > 2):
                print(colored("\nToo many failed attempts... going back.\n", "red"))
                file = 'board_setup\\standard_setup.xlsx'
                game = 0
                break

            print(colored("\nPlease type in a number.", "yellow"))
            fails += 1
            
        except AssertionError:                
            if(game < 0):
                
                if(fails > 2):
                    print(colored("\nToo many failed attempts... going back.\n", "red"))
                    file = 'board_setup\\standard_setup.xlsx'
                    game = 0
                    break
                    
                print(colored("\nThe game you're trying to delete does not exist. Type '-' and the number next to the game you'd like to delete.", "yellow"))
                
            else:
                if(fails > 2):
                    print(colored("\nToo many failed attempts... going back.\n", "red"))
                    file = 'board_setup\\standard_setup.xlsx'
                    game = 0
                    break
                    
                print(colored("\nThe game you're trying to load does not exist. Type the number to the left of the game you want to load.", "yellow"))

            fails += 1
  
    directory_name = 'saves\\' + save_list[game]
    
    if(game < 0):
        print(colored("\nAre you sure you want to delete {}? Press 'Y' to confirm.".format(saved_games[-game]), "yellow"))
        _input = input("Delete? ")
        
        if(_input.upper() == 'Y'):
            shutil.rmtree('saves\\' + save_list[-game])
            print(colored("\n{} has been deleted.".format(saved_games[-game][0]), "red"))
        
        print('\n')
        directory_name = get_directory_name()
        
    if(game == 0):
        print(colored("\nGoing back...", "blue"))
    
    print('\n')
    return directory_name
    
    
def retrieve_properties(directory):
    properties_raw = pd.read_csv(directory)
    properties = {}

    for p in range(len(properties_raw)):
        p_name = properties_raw.loc[p]['property_names'].title()
        p_details = Property(p_name,
                             properties_raw.loc[p]['location'], 
                             properties_raw.loc[p]['color'].lower(),
                             properties_raw.loc[p]['rents'][1:-1].split(','),
                             properties_raw.loc[p]['prices'][1:-1].split(','))

        properties[p_name] = p_details

        properties[p_name].owner = properties_raw.loc[p]['owner']
        properties[p_name].set = properties_raw.loc[p]['set']
        properties[p_name].houses = properties_raw.loc[p]['houses']
        properties[p_name].mortgaged = properties_raw.loc[p]['mortgaged']

    property_names = properties_raw['property_names'].values.astype(str)
    property_names = [property_names[i].title() for i in range(len(property_names))]

    property_locations = properties_raw['location'].values
    
    return properties, property_names, property_locations


def retrieve_railroads(directory):
    railroads_raw = pd.read_csv(directory)
    railroads = {}

    for r in range(len(railroads_raw)):
        r_name = railroads_raw.loc[r]['railroad_names'].title()
        r_details = Railroad(r_name,
                             railroads_raw.loc[r]['location'], 
                             railroads_raw.loc[r]['rents'][1:-1].split(','),
                             railroads_raw.loc[r]['prices'])

        railroads[r_name] = r_details

        railroads[r_name].owner = railroads_raw.loc[r]['owner']
        railroads[r_name].rr_owned = railroads_raw.loc[r]['rr_owned']
        railroads[r_name].mortgaged = railroads_raw.loc[r]['mortgaged']

    railroad_names = railroads_raw['railroad_names'].values.astype(str)
    railroad_names = [railroad_names[i].title() for i in range(len(railroad_names))]

    railroad_locations = railroads_raw['location'].values
    
    return railroads, railroad_names, railroad_locations


def retrieve_utilities(directory):
    utilities_raw = pd.read_csv(directory)
    utilities = {}

    for u in range(len(utilities_raw)):
        u_name = utilities_raw.loc[u]['utility_names'].title()
        u_details = Utility(u_name,
                            utilities_raw.loc[u]['location'], 
                            utilities_raw.loc[u]['rentmult'][1:-1].split(','),
                            utilities_raw.loc[u]['prices'])

        utilities[u_name] = u_details

        utilities[u_name].owner = utilities_raw.loc[u]['owner']
        utilities[u_name].util_owned = utilities_raw.loc[u]['util_owned']
        utilities[u_name].mortgaged = utilities_raw.loc[u]['mortgaged']

    utility_names = utilities_raw['utility_names'].values.astype(str)
    utility_names = [utility_names[i].title() for i in range(len(utility_names))]

    utility_locations = utilities_raw['location'].values
    
    return utilities, utility_names, utility_locations
    
    
def retrieve_space_list(directory):
    space_list = pd.read_csv(directory)
    space_list.index = space_list['Unnamed: 0']
    space_list.index.name = ''
    space_list = space_list.drop('Unnamed: 0', 1)
    return space_list
    
    
def retrieve_players(directory):
    players_raw = pd.read_csv(directory)
    players = []

    for p in range(len(players_raw)):
        p_details = Player(players_raw.loc[p]['name'], players_raw.loc[p]['color'].lower())
        players.append(p_details)

        players[p].money = players_raw.loc[p]['money']
        players[p].position = players_raw.loc[p]['position']
        players[p].properties = players_raw.loc[p]['properties']
        players[p].cards = players_raw.loc[p]['cards']
        players[p].isTurn = players_raw.loc[p]['isTurn']
        players[p].turnCount = players_raw.loc[p]['turnCount']
        players[p].jail = players_raw.loc[p]['jail']
    
    return players
    
    
def retrieve_chance_deck(directory):
    chance_deck = pd.read_csv(directory + '\\chance_deck.csv')
    chance_deck = chance_deck.drop('Unnamed: 0', 1)
    return chance_deck


def retrieve_community_deck(directory):
    community_deck = pd.read_csv(directory + '\\community_deck.csv')
    community_deck = community_deck.drop('Unnamed: 0', 1)
    return community_deck


def retrieve_chance_cards(directory):
    chance_cards = pd.read_csv(directory + '\\chance_cards.csv')
    chance_cards = np.array(chance_cards['0'])
    return chance_cards


def retrieve_community_cards(directory):
    community_cards = pd.read_csv(directory + '\\community_cards.csv')
    community_cards = np.array(community_cards['0'])
    return community_cards


def retrieve_free_parking(directory):
    free_parking = pd.read_csv(directory + '\\free_parking.csv')
    free_parking = np.array(free_parking['0'])
    return free_parking