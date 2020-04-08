from dependencies import *
from monopoly_classes import *
import trade_functions as TF
import board_functions as BF
        
        
def shuffle_chance_cards(player_list, deck_length, first_shuffle = False):
    cards = list(range(deck_length))
    cards = random.sample(cards, deck_length)

    for p in player_list:
        if (p.cards[0] == True):
            cards.remove(0)
    
    if(first_shuffle == False):
        print("Chance cards have been shuffled!")
    
    return cards


def shuffle_community_cards(player_list, deck_length, first_shuffle = False):
    cards = list(range(deck_length))
    cards = random.sample(cards, deck_length)

    for p in player_list:
        if (p.cards[1] == True):
            cards.remove(0)
        
    if(first_shuffle == False):
        print("Community Chest cards have been shuffled!")
    
    return cards


def chance(player, chance_cards, chance_deck):

    if(chance_cards == []):
        chance_cards = shuffle_chance_cards()
        
    c = chance_cards[0]
    chance_cards.remove(c)
        
    print("The card reads:", chance_deck.loc[c]['Description'])
    setPos, money_earn, note = chance_deck.loc[c][1:]
           
    if(note == 'KEEP'):
        player.cards[0] = True
        print("This card can be kept until needed or sold.")
           
    elif(note == 'REPAIR'):
        if player.properties is None:
            pass
        else:
            if(player.properties[0].houses == 5):
                money_earn = -100
        
            else:
                sum_houses = player.properties[0].houses
            
                for po in range(1,len(player.properties)):
                    if(player.properties[po].houses == 5):
                        money_earn -= 100
                
                    else:
                        sum_houses += props[po].add_houses(props[po+1]) 
            
                money_earn -= (sum_houses * 25)
                print("A total of", -(money_earn), "dollars is due.")
                
    elif(note == 'PLAYER'):
        for p in players:
            p.money -= money_earn
        money_earn = len(players) * money_earn
        
    elif(note == 'BACK'):
        setPos = player.position - 3
        
    elif(note == 'UTILITY'):
        if(player.position == 22):
            setPos = 28
        else:
            setPos = 12
            
    elif(note == 'RAILROAD'):
        if(player.position == 7):
            setPos = 15
        elif(player.position == 22):
            setPos = 25
        else:
            setPos = 5
        
    if(money_earn < 0 and note != 'PLAYER'):
        free_parking -= money_earn
        
    return setPos, money_earn


def community_chest(player, community_cards, community_deck):

    if(community_cards == []):
        community_cards = shuffle_community_cards()
        
    cc = community_cards[0]
    community_cards.remove(cc)
        
    print("The card reads:", community_deck.loc[cc]['Description'])
    setPos, money_earn, note = community_deck.loc[cc][1:]
           
    if(note == 'KEEP'):
        player.cards[1] = True
        print("This card can be kept until needed or sold.")
           
    elif(note == 'REPAIR'):
        if player.properties is None:
            pass
        else:
            if(player.properties[0].houses == 5):
                money_earn = -115
        
            else:
                sum_houses = player.properties[0].houses
            
                for po in range(1,len(player.properties)):
                    if(player.properties[po].houses == 5):
                        money_earn -= 115
                
                    else:
                        sum_houses += props[po].add_houses(props[po+1]) 
            
                money_earn -= (sum_houses * 40)
                print("A total of", -(money_earn), "dollars is due.")
                
    elif(note == 'PLAYER'):
        for p in players:
            p.money = p.money - money_earn
        money_earn = len(players) * money_earn 
        
    if(money_earn < 0 and note != 'PLAYER'):
        free_parking = free_parking - money_earn
        
    return setPos, money_earn
    
    
def controls(player):
    
    print(colored("\nHere are the controls you need to play:", player.color))
    print(colored("<just hit enter> - roll the dice / continue", player.color))
    print(colored("[?] - controls menu", player.color))
    print(colored("[me] - get information on your character", player.color))
    print(colored("[B] - board: view the game board", player.color))
    print(colored("[T] - trade: propose a trade with a fellow player", player.color))
    print(colored("[O] - overview: see how each player is doing", player.color))
    print(colored("[P] - properties: see information on your properties, others' properties, and unclaimed properties", player.color))
    print(colored("[C] - color: change your color", player.color))
    print(colored("[S] - save: save game for later", player.color))
    print(colored("[quit] - end game", player.color))
        
        
def me(player, space_list):
    print("\n")
    print(colored(player.name, player.color))
    print(colored("Money: {}".format(player.money), player.color))
    print(colored("Current Position: {} ({})".format(player.position, space_list.iloc[player.position][0]), player.color))
    
    props = []
    if(player.properties == []):
        props.append('None')
    else:
        for p in player.properties:
            props.append(p)
    print(colored("Properties: {} -- For more property information, type [P].".format(props), player.color))
    
    cards = []
    if(player.cards[0] == True):
        cards.append('Chance')
    if(player.cards[1] == True):
        cards.append('Community Chest')
    if(True not in player.cards):
        cards.append('None')
    
    print(colored("Get out of jail free cards: {}".format(cards), player.color))
    
    print(colored("Number of doubles rolled in a row: {}".format(player.turnCount), player.color))
    
    print("\n")
    
    
def view_properties(player, properties, property_names, other_params):
    print(colored("\nPlease type the beginning of the property name you want to search or hit enter to view them all!", player.color))
    
    property_search = input("Property: ").title()
    properties_list = [i for i in property_names if property_search in i]
    
    for prop in properties_list:
        prop = prop.title()
        print(colored("\n==================\n {} \n==================".format(prop), player.color)) 
        print(colored("Color: {}".format(properties[prop].color), player.color))
        print(colored("Location: {}".format(properties[prop].location), player.color))
        print(colored("Owner: {}".format(properties[prop].owner), player.color))

        print(colored("\nPrice Overview: {} + {} per house".format(properties[prop].prices[0], properties[prop].prices[1]), player.color))
        
        houseStatus = properties[prop].houses
        if(properties[prop].owner == None): houseStatus = 'unowned'
        elif(properties[prop].set == False): houseStatus = '0 (individual)'
        elif(houseStatus == other_params['houses_for_hotel']): houseStatus = 'HOTEL'
        elif(houseStatus > other_params['houses_for_hotel']): houseStatus = 'HOTEL+{}'.format(houseStatus - other_params['houses_for_hotel'])
        print(colored("Number of Houses: {}".format(houseStatus), player.color))

        current_investment = (properties[prop].prices[0] * (properties[prop].owner != None)) + (properties[prop].prices[1]*properties[prop].houses)
        print(colored("Current Investment: {}".format(current_investment), player.color))
        
        rents = properties[prop].rents
        print(colored("\nCurrent Rent: {}".format(properties[prop].get_currentRent()), player.color))

        _ = ['- Individual:', '- Monopoly:', '- 1 House:'] 
        
        for h in range(2, other_params['houses_for_hotel']):
            _.append('- {} Houses:'.format(h))
            
        _.append('- Hotel:')
        
        for h in range(1, len(rents) - other_params['houses_for_hotel'] - 1):
            _.append('- Hotel+{}:'.format(h))
        
        print(colored("\nPotential Rents:", player.color))
        print(colored(pd.DataFrame(rents, _, columns = ['']), player.color))
        print("\n")
        
    
    
def change_color(player):
    print("\n")
    print(colored("Which color would you like to use?", player.color))
    print("Available colors include: '{}', '{}', '{}', '{}', '{}', '{}', and '{}'.".format(colored("grey", "grey"), \
        colored("red", "red"), colored("green", "green"), colored("yellow", "yellow"), colored("blue", "blue"), \
        colored("magenta", "magenta"), colored("cyan", "cyan")))
          
    c = input("Color: ").lower()
    
    fails = 0
    while(c not in ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan']):
        fails = fails + 1
        if(fails > 3):
            print("Too many failed attempts... exiting.")
            player.color = player.color
            return None
    
    player.color = c
    print(colored("\nDone!", c))
    
    
def trade(player, players):
    print("\n")
    
    d_player = TF.desired_player(player = player, players = players)
    d_property, is_card = TF.desired_property(player = player, players = players, d_player = d_player)
    d_method = TF.desired_method(player = player, players = players, d_player = d_player, d_property = d_property, 
                              is_card = is_card, player_offered = None)
    d_offer = TF.desired_offer(player = player, players = players, d_player = d_player, d_property = d_property, 
                            is_card = is_card, d_method = d_method, player_offered = None)
    response, player_offered = TF.offer_delivery(player = player, players = players, d_player = d_player,
                                              d_property = d_property, is_card = is_card, d_offer = d_offer)
    counter = TF.offer_action(player = player, players = players, d_property = d_property, is_card = is_card, 
                           d_offer = d_offer, player_offered = player_offered, response = response, counter = False)
    
    if(counter == True):
        c_method = TF.desired_method(player = player, players = players, d_player = d_player, d_property = d_property, 
                                  is_card = is_card, player_offered = player_offered, counter = True)
        c_offer = TF.desired_offer(player = player, players = players, d_player = d_player, d_property = d_property, 
                                is_card = is_card, d_method = c_method, player_offered = player_offered, counter = True)
        c_response = TF.c_offer_delivery(player = player, players = players, d_player = d_player, d_property = d_property,
                                         is_card = is_card, d_offer = c_offer, player_offered = player_offered)
        TF.offer_action(player = player, players = players, d_property = d_property, is_card = is_card, d_offer = d_offer,
                     player_offered = player_offered, response = c_response, counter = True)
        
        
def board(players, properties, railroads, utilities, space_list):
    side_length = math.ceil(len(space_list)/4) + 1

    BF.h_portion(players = players, properties = properties, railroads = railroads, utilities = utilities, space_list = space_list,
                 start = 2*side_length - 2, increment = 1, length = side_length, position = 'top')
    BF.v_portion(players = players, properties = properties, railroads = railroads, utilities = utilities, space_list = space_list,
                 left = 2*side_length - 3, right = 3*side_length - 2, length = side_length, special_row = 'first')

    r = 3*side_length - 1
    for l in range(2*side_length - 4, side_length, - 1): 
        BF.v_portion(players = players, properties = properties, railroads = railroads, utilities = utilities, space_list = space_list,
                     left = l, right = r, length = side_length)
        r += 1

    BF.v_portion(players = players, properties = properties, railroads = railroads, utilities = utilities, space_list = space_list,
                 left = side_length, right = 4 * side_length - 5, length = side_length, special_row = 'last')
    BF.h_portion(players = players, properties = properties, railroads = railroads, utilities = utilities, space_list = space_list,
                 start = side_length - 1, increment = -1, length = side_length, position = 'bottom')