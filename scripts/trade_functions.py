from dependencies import *

def desired_player(player, players):
    
    print(colored("Type in the number corresponding to the player you would like to trade with:\n", player.color))
    print('[0] GO BACK\n')

    for play in range(len(players)):
        
        if(players[play] == player):
            print('[*]', end = ' ')
            print(colored("{} - ${}", players[play].color).format(players[play].name, players[play].money))
            print(colored("    <cannot trade self>", players[play].color))
            continue
            
        print("[{}]".format(play + 1), end = ' ') 
        print(colored("{} - ${}", players[play].color).format(players[play].name, players[play].money))

        if(players[play].properties == []):
            print(colored("    <no properties>", players[play].color))

        else:
            for prop in range(len(players[play].properties)):
                print(colored("    {}: {}", players[play].color).format(players[play].properties[prop].name, 
                                                                        players[play].properties[prop].color))

        if(players[play].cards[0] == True):
            print(colored("    GET OUT OF JAIL FREE CARD (chance)", players[play].color))

        if(players[play].cards[1] == True):
            print(colored("    GET OUT OF JAIL FREE CARD (community)", players[play].color))

        print('')

    fails = 0

    while(True):
        try:
            d_player = int(input('# '))
            
            if(d_player == 0):
                return 0
            
            assert (d_player >= 0) and (d_player < (len(players) + 1) and (players[d_player - 1] != player))
            break

        except ValueError:
            if(fails > 2):
                print(colored("\nToo many failed attempts... going back.\n", "red"))
                return 0

            print(colored("\nPlease type in a number.", "yellow"))
            fails += 1

        except AssertionError:                
            if(fails > 2):
                print(colored("\nToo many failed attempts... going back.\n", "red"))
                return 0
                
            try:
                if(players[d_player - 1] == player):
                    print(colored("\nYou cannot trade with yourself!", "yellow"))

            except IndexError:
                if(fails > 2):
                    print(colored("\nToo many failed attempts... going back.\n", "red"))
                    return 0
            
                print(colored("\nThe player you're trying to trade with does not exist. Type the number to the left of the player you want to trade.", "yellow"))
            
            fails += 1
            
    return d_player


def desired_property(player, players, d_player):
    
    if(d_player == 0):
        return 0, False
    
    print(colored("\nType in the number corresponding to the property or card you would like to trade for:\n", player.color))
    print(colored("[0] GO BACK\n", player.color))
    
    count = 1

    for prop in range(len(players[d_player - 1].properties)):
        
        print(colored("[{}] {}", player.color).format(count, players[d_player - 1].properties[prop].name))
        if(players[d_player-1].properties[prop].mortgaged == True):
            print(colored("    * UNMORTGAGING THIS PROPERTY AT TIME OF PURCHASE WILL COST ${}. *", player.color).format(int(players[d_player - 1].properties[prop].prices[0] / 2 * 1.1)))
            print(colored("    * UNMORTGAGING THIS PROPERTY AFTERWARDS WILL COST AN ADDITIONAL ${}, DUE AT TIME OF PURCHASE. *\n", player.color).format(int(players[d_player - 1].properties[prop].prices[0] / 2 * 0.1)))
        else:
            print('')
                
            
        print(colored("    Color: {}", player.color).format(players[d_player - 1].properties[prop].color))

        rents = str(['$' + r for r in [str(r) for r in players[d_player - 1].properties[prop].rents]])[1:-1]
        print(colored("    Rents: {}", player.color).format(rents))

        print(colored("    Prices: ${} + ${}/house", player.color).format(players[d_player - 1].properties[prop].prices[0], 
                                                                          players[d_player - 1].properties[prop].prices[1]))
        print('\n')

        count += 1

    if(players[d_player - 1].cards[0] == True):
        print(colored("[{}] GET OUT OF JAIL FREE CARD (chance)", player.color).format(count))
        print(colored("    Value: $50\n", player.color))
        count += 1

    if(players[d_player - 1].cards[1] == True):
        print(colored("[{}] GET OUT OF JAIL FREE CARD (community)", player.color).format(count))
        print(colored("    Value: $50\n", player.color))
        count += 1
    
    fails = 0

    while(True):
        try:
            d_property = int(input('# '))
            assert ((d_property >= 0) and (d_property < count))
            break

        except ValueError:
            if(fails > 2):
                print(colored("\nToo many failed attempts... going back.\n", "red"))
                return 0, False

            print(colored("\nPlease type in a number.", "yellow"))
            fails += 1

        except AssertionError:                
            if(fails > 2):
                print(colored("\nToo many failed attempts... going back.\n", "red"))
                return 0, False

            print(colored("\nThe property or card you're requesting does not exist. Type the number to the left of the property or card you'd like.", "yellow"))

            fails += 1
    
    if(d_property > len(players[d_player - 1].properties)):
        is_card = True
    else:
        is_card = False
       
    return d_property, is_card


def desired_method(player, players, d_player, d_property, is_card, player_offered, counter = False):

    if(d_property == 0):
        return [0]
 
    #####################
    # FOR COUNTER OFFER #
    if(counter == True):
        if(is_card == True):
            print(colored("\nWhich would you like {} to offer for the GET OUT OF JAIL FREE CARD?\nYou can select multiple options by typing in two numbers (e.g. '12')\n", 
                  player_offered.color).format(player.name))
        else:
            print(colored("\nWhich would you like {} to offer for {}?\nYou can select multiple options by typing in two numbers separated by a comma (e.g. '1,2').\n", 
                          player_offered.color).format(player.name,
                          players[d_player - 1].properties[d_property - 1].name))
            
            print(colored("[0] GO BACK\n", player_offered.color))

            count = 1

            if(player.money > 0):
                print(colored("[{}] Money", player_offered.color).format(count))
                count += 1

            if(player.properties != []):
                print(colored("[{}] Property", player_offered.color).format(count))
                count += 1

            if(player.cards != [False, False]):
                print(colored("[{}] Get out of jail card(s)", player_offered.color).format(count))

            print(' ')
    #####################
    
    else:
        if(is_card == True):    
            print(colored("\nWhich would you like to offer {} for the GET OUT OF JAIL FREE CARD?\nYou can select multiple options by typing in two numbers (e.g. '12')\n", 
                  player.color).format(players[d_player - 1].name))
        else:
            print(colored("\nWhich would you like to offer {} for {}?\nYou can select multiple options by typing in two numbers separated by a comma (e.g. '1,2').\n", 
                      player.color).format(players[d_player - 1].name,
                      players[d_player - 1].properties[d_property - 1].name))
        
        print(colored("[0] GO BACK\n", player.color))

        count = 1

        if(player.money > 0):
            print(colored("[{}] Money", player.color).format(count))
            count += 1

        if(player.properties != []):
            print(colored("[{}] Property", player.color).format(count))
            count += 1

        if(player.cards != [False, False]):
            print(colored("[{}] Get out of jail card(s)", player.color).format(count))

        print(' ')
    
    fails = 0
    
    while(True):
        try:
            d_method = input("# ").split(',')
            d_method = [int(o) for o in list(d_method)]
            assert set(d_method).issubset(range(4))
            break

        except ValueError:
            if(fails > 2):
                if(counter == True):
                    print(colored("\nToo many failed attempts... declining.\n", "red"))
                    return 0
                else:
                    print(colored("\nToo many failed attempts... going back.\n", "red"))
                    return 0

            print(colored("\nPlease type in a number.", "yellow"))
            fails += 1

        except AssertionError:                
            if(fails > 2):
                if(counter == True):
                    print(colored("\nToo many failed attempts... declining.\n", "red"))
                    return 0
                else:
                    print(colored("\nToo many failed attempts... going back.\n", "red"))
                    return 0

            print(colored("\nThe offer type you've chosen does not exist. Type the number to the left of the type of offer you'd like to make.", "yellow"))

            fails += 1

    
    return d_method


def desired_offer(player, players, d_player, d_property, is_card, d_method, player_offered, counter = False):
    
    money = 0
    props = []
    cards = []
    
    if(0 in d_method):
        return money, props, cards
    
    #####################
    # FOR COUNTER OFFER #
    if(counter == True):
        if(is_card == True):
            print(colored("\nIn exchange for the GET OUT OF JAIL FREE CARD...\n", player_offered.color))
        
        else:
            print(colored("\nIn exchange for {}...\n", player_offered.color).format(players[d_player - 1].properties[d_property - 1].name))
    #####################    
        
        
    else:
        if(is_card == True):
            print(colored("\nIn exchange for a GET OUT OF JAIL FREE CARD from {}...\n", player.color).format(players[d_player - 1].name))
        
        else:
            print(colored("\nIn exchange for {} from {}...\n", player.color).format(players[d_player - 1].properties[d_property - 1].name,
                                                                              players[d_player - 1].name))
        
    
    if(1 in d_method):
        if(counter == True):
            print(colored("How much money would you like {} to offer? Type '0' if you no longer want money.\n", 
                          player_offered.color).format(player.name))
        else:
            print(colored("How much money would you like to offer? Type '0' if you no longer want to offer money.\n",
                          player.color))
        
        fails = 0

        while(True): 
            try:
                money = int(input('$'))
                assert money <= player.money
                break

            except ValueError:
                if(fails > 2):
                    if(counter == True):
                        print(colored("\nToo many failed attempts... declining.\n", "red"))
                        return 0, [], []
                    else:
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []

                print(colored("\nPlease type in a number.", "yellow"))
                fails += 1

            except AssertionError:                
                if(fails > 2):
                    if(counter == True):
                        print(colored("\nToo many failed attempts... declining.\n", "red"))
                        return 0, [], []
                    else:
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []

                print(colored("\nYou don't have enough money to do that!", "yellow"))

                fails += 1

            print('')

    if(2 in d_method):
        #####################
        # FOR COUNTER OFFER #
        if(counter == True):
            print(colored("\nWhich property or properties would you like {} to offer?", player_offered.color).format(player.name))
            
            if(len(player.properties) > 1):
                print(colored("You can select multiple options by typing in two numbers separated by a comma (e.g. '1,2').\n", 
                              player_offered.color))
            
            print(colored("[0] NONE\n", player_offered.color))

            count = 1

            for prop in range(len(player.properties)):

                print(colored("[{}] {}", player_offered.color).format(count, player.properties[prop].name), end = ' ')

                if(player.properties[prop].mortgaged == True):
                    print(colored("    * UNMORTGAGING THIS PROPERTY AT TIME OF PURCHASE WILL COST ${}. *", player_offered.color).format(int(player.properties[prop-1].prices[0] / 2 * 1.1)))
                    print(colored("    * UNMORTGAGING THIS PROPERTY AFTERWARDS WILL COST AN ADDITIONAL ${}, DUE AT TIME OF PURCHASE. *\n", player_offered.color).format(int(player.properties[prop-1].prices[0] / 2 * 0.1)))

                else:
                    print("\n")

                print(colored("    Color: {}", player_offered.color).format(player.properties[prop].color))

                rents = str(['$' + r for r in [str(r) for r in player.properties[prop].rents]])[1:-1]
                print(colored("    Rents: {}", player_offered.color).format(rents))

                print(colored("    Prices: ${} + ${}/house", player_offered.color).format(player.properties[prop].prices[0], 
                                                                                  player.properties[prop].prices[1]))
                print('')

                count += 1
        #####################
        
        else:
            print(colored("\nWhich property or properties would you like to offer?", player.color))
        
            if(len(player.properties) > 1):
                print(colored("You can select multiple options by typing in two numbers separated by a comma (e.g. '1,2').\n", 
                              player.color))

            print(colored("[0] NONE\n", player.color))

            count = 1

            for prop in range(len(player.properties)):

                print(colored("[{}] {}", player.color).format(count, player.properties[prop].name), end = ' ')

                if(player.properties[prop].mortgaged == True):
                    print(colored("(Mortgaged)", player.color))

                else:
                    print("\n")

                print(colored("    Color: {}", player.color).format(player.properties[prop].color))

                rents = str(['$' + r for r in [str(r) for r in player.properties[prop].rents]])[1:-1]
                print(colored("    Rents: {}", player.color).format(rents))

                print(colored("    Prices: ${} + ${}/house", player.color).format(player.properties[prop].prices[0], 
                                                                                  player.properties[prop].prices[1]))
                print('')

                count += 1

        fails = 0

        while(True):
            try:
                props = input("# ").split(',')
                props = set([int(p) for p in list(props)])
                assert props.issubset(range(len(player.properties) + 1))
                break

            except ValueError:
                if(fails > 2):
                    if(counter == True):
                        print(colored("\nToo many failed attempts... declining.\n", "red"))
                        return 0, [], []
                        
                    else:
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []

                print(colored("\nPlease type in a number.", "yellow"))
                fails += 1

            except AssertionError:                
                if(fails > 2):
                    if(counter == True):
                        print(colored("\nToo many failed attempts... declining.\n", "red"))
                        return 0, [], []
                    
                    else:
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []

                print(colored("\nThe property you've chosen does not exist. Type the number to the left of the property you'd like to trade.", "yellow"))

                fails += 1

    if(3 in d_method):
        #####################
        # FOR COUNTER OFFER #
        if(counter == True):
            print(colored("\nWhich GET OUT OF JAIL FREE CARD would you like {} to offer?", player_offered.color).format(player.name))
        
            if(sum(player.cards) == 2):
                print(colored("You can select multiple options by typing in two numbers separated by a comma (e.g. '1,2').",
                              player_offered.color))
        
            print(colored("\n[0] NONE\n", player_offered.color))

            count = 1

            if(player.cards[0] == True):
                print(colored("[{}] CHANCE", player_offered.color).format(count))
                count += 1

            if(player.cards[1] == True):
                print(colored("[{}] COMMUNITY CHEST", player_offered.color).format(count))
        #####################
        
        else:
            print(colored("\nWhich GET OUT OF JAIL FREE CARD would you like to offer?", player.color))

            if(sum(player.cards) == 2):
                print(colored("You can select multiple options by typing in two numbers separated by a comma (e.g. '1,2').",
                              player.color))

            print(colored("\n[0] NONE\n", player.color))

            count = 1

            if(player.cards[0] == True):
                print(colored("[{}] CHANCE", player.color).format(count))
                count += 1

            if(player.cards[1] == True):
                print(colored("[{}] COMMUNITY CHEST", player.color).format(count))

        fails = 0
    
        while(True):
            try:
                cards = input("\n# ").split(',')
                cards = set([int(c) for c in list(cards)])
                cards_adj = [c - 1 for c in props]
                assert cards.issubset(range(len(player.cards) + 1))
                break

            except ValueError:
                if(fails > 2):
                    if(counter == True):
                        print(colored("\nToo many failed attempts... declining.\n", "red"))
                        return 0, [], []
                    else:
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []

                print(colored("\nPlease type in a number.", "yellow"))
                fails += 1

            except AssertionError:                
                if(fails > 2):
                    if(counter == True):
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []
                    
                    else:
                        print(colored("\nToo many failed attempts... going back.\n", "red"))
                        return 0, [], []

                print(colored("\nThe card you've chosen does not exist. Type the number to the left of the card you'd like to trade.", "yellow"))

                fails += 1

            print('')
        
    #####################
    # FOR COUNTER OFFER #
    if(counter == True):
        
        if((money == 0) and (props == {0} or len(props) == 0) and (cards == {0} or len(cards) == 0)):
            print(colored("\nCounter offer aborted.", "red"))
            return 0, [], []
        
        print(colored("\nPress [Y] to confirm your counter offer:\n", player_offered.color))

        if(money > 0):
            print(colored("Money: ${}", player_offered.color).format(money))
        if(props != {0} and len(props) > 0):
            print(colored("Properties: ", player_offered.color), end = '')
            [print(colored(player.properties[p-1].name, player_offered.color), end = '     ') for p in props]
        if(cards != {0} and len(cards) > 0):
            print(colored("GET OUT OF JAIL FREE CARD - ", player_offered.color), end = '')

            if(1 in cards):
                print(colored("chance    ", player_offered.color))
            if(2 in cards):
                print(colored("community chest", player_offered.color))

        print('\n')

        response = input().upper()

        if(response.startswith('Y')):
            print(colored("\nSending counter offer!", "green"))
            return money, props, cards

        else:
            print(colored("You have selected to NOT confirm this counter offer. Hit enter to continue or type anything to confirm.", "red"))
            response = input().upper()

            if(response == ''):  
                print(colored("Counter offer aborted.", "red"))
                return 0, [], []

            else:
                print(colored("\nSending counter offer!", "green"))
                return money, props, cards
    #####################  
    
    else:
        if((money == 0) and (props == {0} or len(props) == 0) and (cards == {0} or len(cards) == 0)):
            print(colored("\nTrade request aborted.", "red"))
            return 0, [], []
        
        print(colored("\nPress [Y] to confirm your trade request:\n", player.color))

        if(money > 0):
            print(colored("Money: ${}", player.color).format(money))
        if(props != {0} and len(props) > 0):
            print(colored("Properties: ", player.color), end = '')
            [print(colored(player.properties[p-1].name, player.color), end = '     ') for p in props]
        if(cards != {0} and len(cards) > 0):
            print(colored("GET OUT OF JAIL FREE CARD - ", player.color), end = '')

            if(1 in cards):
                print(colored("chance    ", player.color))
            if(2 in cards):
                print(colored("community chest", player.color))

        print('\n')

        response = input().upper()

        if(response.startswith('Y')):
            print(colored("\nSending trade request!", "green"))
            return money, props, cards

        else:
            print(colored("You have selected to NOT confirm this trade request. Hit enter to continue or type anything to confirm.", "red"))
            response = input().upper()

            if(response == ''):  
                print(colored("Trade request aborted.", "red"))
                return 0, [], []

            else:
                print(colored("\nSending trade request!", "green"))
                return money, props, cards
            
            
def offer_delivery(player, players, d_player, d_property, is_card, d_offer):
    
    if(d_offer[0] == 0 and (len(d_offer[1]) == 0 or d_offer[1] == {0}) and (len(d_offer[2]) == 0 or d_offer[2] == {0})):
        return 'D', None
    
    player_offered = players[d_player - 1]
    
    if(is_card == True):
        if(player_offered.cards[0] == False or player_offered.cards[1] == False):
            print(colored("\n{}, {} has proposed a trade for your GET OUT OF JAIL FREE CARD.", 
                          player_offered.color).format(player_offered.name, player.name))
        else:
            if(d_property - len(player_offered.properties) - 1 == 0):
                print(colored("\n{}, {} has proposed a trade for your GET OUT OF JAIL FREE CARD (chance).", 
                          player_offered.color).format(player_offered.name, player.name))
            else:
                print(colored("\n{}, {} has proposed a trade for your GET OUT OF JAIL FREE CARD (community chest).", 
                          player_offered.color).format(player_offered.name, player.name))
    
    else:
        print(colored("\n{}, {} has proposed a trade for {}:", player_offered.color).format(player_offered.name, 
                                                         player.name, player_offered.properties[d_property - 1].name))
    
    if(d_offer[0] > 0):
        print(colored("\nMoney: ${}", player_offered.color).format(d_offer[0]))
    
    if(len(d_offer[1]) > 0 and d_offer[1] != {0}):
        print(colored("\nProperties:\n", player_offered.color))
        
        for prop in d_offer[1]:

            print(colored("{}", player_offered.color).format(player.properties[prop-1].name))
                
            if(player.properties[prop-1].mortgaged == True):
                print(colored("* UNMORTGAGING THIS PROPERTY AT TIME OF PURCHASE WILL COST ${}. *", player_offered.color).format(int(player.properties[prop-1].prices[0] / 2 * 1.1)))
                print(colored("* UNMORTGAGING THIS PROPERTY AFTERWARDS WILL COST AN ADDITIONAL ${}, DUE AT TIME OF PURCHASE. *\n", player_offered.color).format(int(player.properties[prop-1].prices[0] / 2 * 0.1)))
                
            else:
                print('')

            print(colored("Color: {}", player_offered.color).format(player.properties[prop].color))

            rents = str(['$' + r for r in [str(r) for r in player.properties[prop].rents]])[1:-1]
            print(colored("Rents: {}", player_offered.color).format(rents))

            print(colored("Prices: ${} + ${}/house", player_offered.color).format(player.properties[prop].prices[0], 
                                                                              player.properties[prop].prices[1]))
            print('')
        
    if(len(d_offer[2]) > 0 and d_offer[2] != {0}):
        print(colored("GET OUT OF JAIL FREE CARD - ", player_offered.color), end = '')
    
        if(1 in d_offer[2]):
            print(colored("chance    ", player_offered.color))
        if(2 in d_offer[2]):
            print(colored("community chest", player_offered.color))
        
    print(colored("\nWould you like to accept, decline, or counter this proposal?", player_offered.color))
    print(colored("\n[A] Accept\n[D] Decline\n[C] Counter\n", player_offered.color))
    
    response = input("A/D/C: ").upper()
    fails = 0
    
    while(response not in ['A', 'D', 'C']):
        if(fails > 2):
            print(colored("Too many failed attempts... declining.", "red"))
            return 'D', None
        
        print(colored("Please type 'A' to accept, 'D' to decline, or 'C' to counter.", "yellow"))
        response = input("A/D/C: ").upper()
        
        fails += 1
        
    return response, player_offered


def c_offer_delivery(player, players, d_player, d_property, is_card, player_offered, d_offer): ###FOR COUNTER OFFERS###
    
    if(d_offer[0] == 0 and (len(d_offer[1]) == 0 or d_offer[1] == {0}) and (len(d_offer[2]) == 0 or d_offer[2] == {0})):
        return 'D'
    
    if(is_card == True):
        if(player_offered.cards[0] == False or player_offered.cards[1] == False):
            print(colored("\n{}, {} has proposed a counter offer for the GET OUT OF JAIL FREE CARD.", 
                          player.color).format(player.name, player_offered.name))
        else:
            if(d_property - len(player_offered.properties) - 1 == 0):
                print(colored("\n{}, {} has proposed a counter offer for the GET OUT OF JAIL FREE CARD (chance).", 
                          player.color).format(player.name, player_offered.name))
            else:
                print(colored("\n{}, {} has proposed a counter offer for the GET OUT OF JAIL FREE CARD (community chest).", 
                          player.color).format(player.name, player_offered.name))
    
    else:
        print(colored("\n{}, {} has proposed a counter offer for {}:", player.color).format(player.name, 
                                                         player_offered.name, player_offered.properties[d_property - 1].name))
    
    if(d_offer[0] > 0):
        print(colored("\nMoney: ${}", player.color).format(d_offer[0]))
    
    if(len(d_offer[1]) > 0 and d_offer[1] != {0}):
        print(colored("\nProperties:\n", player.color))
        
        for prop in d_offer[1]:

            print(colored("{}", player.color).format(player.properties[prop-1].name), end = '')
                
            if(player.properties[prop-1].mortgaged == True):
                print(colored("(Mortgaged)", player.color))
                
            else:
                print('')

            print(colored("Color: {}", player.color).format(player.properties[prop].color))

            rents = str(['$' + r for r in [str(r) for r in player.properties[prop].rents]])[1:-1]
            print(colored("Rents: {}", player.color).format(rents))

            print(colored("Prices: ${} + ${}/house", player.color).format(player.properties[prop].prices[0], 
                                                                              player.properties[prop].prices[1]))
            print('')
        
    if(len(d_offer[2]) > 0 and d_offer[2] != {0}):
        print(colored("GET OUT OF JAIL FREE CARD - ", player.color), end = '')
    
        if(1 in d_offer[2]):
            print(colored("chance    ", player.color))
        if(2 in d_offer[2]):
            print(colored("community chest", player.color))
        
    print(colored("\nWould you like to accept or decline this counter offer?", player.color))
    print(colored("You can counter this counter offer by declining and reattempting to trade.", player.color))
    print(colored("\n[A] Accept\n[D] Decline\n", player.color))
    
    response = input("A/D: ").upper()
    fails = 0
    
    while(response not in ['A', 'D']):
        if(fails > 2):
            print(colored("Too many failed attempts... declining.", "red"))
            return 'D'
        
        print(colored("Please type 'A' to accept or 'D' to decline", "yellow"))
        response = input("A/D: ").upper()
        
        fails += 1
        
    return response


def offer_action(player, players, d_property, is_card, d_offer, player_offered, response, counter):

    if(response == 'A'):
        
        if(is_card == False):
            player.properties.append(player_offered.properties[d_property - 1])
            player_offered.properties.remove(player_offered.properties[d_property - 1])
        else:
            if(d_property - 1 - len(player_offered.properties) == 0):
                player.cards[0] = True
                player_offered.cards[0] = False
            else:
                player.cards[1] = True
                player_offered.cards[0] = False
        
        player_offered.money += d_offer[0]
        player.money -= d_offer[0]
        
        props_exchanged = [player.properties[p-1] for p in range(len(player.properties)) if p in d_offer[1]]
        player_offered.properties.extend(props_exchanged)
        
        for pe in range(len(props_exchanged)):
            player.properties.remove(props_exchanged[pe])
        
        if(0 in d_offer[2]):
            player_offered.cards[0] = True
            player.cards[0] = False
            
        if(1 in d_offer[2]):
            player_offered.cards[1] = True
            player.cards[1] = False
            
        if(counter == True):
            print(colored("Counter offer accepted!", "green"))
        else:
            print(colored("\n{}, {} has accepted your offer.\n", "green").format(player.name, player_offered.name))
            
        return False
            
    if(response == 'D'):
        if(counter == True):
            print(colored("Counter offer declined.", "red"))
            
        else:
            if(player_offered != None):
                print(colored("\n{}, {} has declined your offer.\n", "red").format(player.name, player_offered.name))
            
            else:
                print(colored("\nTrade aborted.", "red"))
        
        return False
    
    if(response == 'C'):
        return True