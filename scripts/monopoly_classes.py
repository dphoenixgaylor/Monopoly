from dependencies import *
from gameplay_functions import chance, community_chest

class Player:
    def __init__(self, name, color, other_params):
        self.name = name
        self.color = color
        self.money = other_params['starting_money']
        self.position = 0
        self.properties = []
        self.cards = [False, False]
        self.turnCount = 0
        self.jail = -1
    
    def move_position(self, other_params, space_list, specials):
        roll = []
        double = False
        
        for d in range(len(other_params['dice_sizes'])):
            r = random.randrange(1, other_params['dice_sizes'][d] + 1)
            roll.append(r)
        
        total = sum(roll)
        
        print(colored("{} rolled a {}".format(self.name, roll[0]), self.color), end = '')
        
        for r in range(1, len(other_params['dice_sizes']) - 1):
            print(colored(", a {}".format(roll[r]), self.color), end = '') 
        
        if len(other_params['dice_sizes']) > 2:
            print(colored(", and a {} and moves {} spaces.".format(roll[len(other_params['dice_sizes'])-1], sum(roll)), self.color))
            
        elif len(other_params['dice_sizes']) == 2:
            print(colored(" and a {} and moves {} spaces.".format(roll[len(other_params['dice_sizes'])-1], sum(roll)), self.color))
            
        self.position = self.position + sum(roll)
        
        if(len(set(roll)) == 1):
            double = True
            self.turnCount = self.turnCount + 1
            
            if(self.turnCount == other_params['doubles_before_jail']):
                self.position = -1
                double = False
                self.turnCount = 0
                print(colored("{} has rolled matching dice {} times in a row and has been sent to jail!".format(self.name, other_params['doubles_before_jail']), "red"))
                return double
                
        else:
            self.turnCount = 0
        
        if(self.position > (len(space_list) - 1)):
            print(colored("{} passed GO and collects ${}!".format(self.name, int(specials[specials['Name'] == 'GO']['MoneyEarned'].values[0])), self.color))
            self.money += int(specials[specials['Name'] == 'GO']['MoneyEarned'].values[0])
            print(colored("{} now has {} dollars".format(self.name, self.money), self.color))
            self.position -= len(space_list)
        
        return double
            
            
    def landing(self, specials, chance_cards, community_cards, chance_deck, community_deck):
        original_position = self.position
        
        # Chance and Community Chest
        CH_values = specials[specials['Name'] == 'CHANCE']['Location'].values
        CM_values = specials[specials['Name'] == 'COMMUNITY']['Location'].values
        
        if((self.position in CH_values) | (self.position in CM_values)):
            
            if(self.position in CH_values):
                print(colored("{} landed on Chance!".format(self.name), self.color))
                setPos, money_earn = chance(self, chance_cards = chance_cards, chance_deck = chance_deck)
            
            else:
                print(colored("{} landed on Community Chest!".format(self.name), self.color))
                setPos, money_earn = community_chest(self, community_cards = community_cards, community_deck = community_deck)
            
            if(math.isnan(setPos) == False):
                self.position = setPos
                
                if((self.position < original_position) and self.position != -1):
                    money_earn += int(specials[specials['Name'] == 'GO']['MoneyEarned'].values[0])
                    print(colored("{} passed GO and collects ${}!".format(self.name, money_earn), self.color))
                
            self.money = self.money + money_earn
            
            if(money_earn != 0):
                print(colored("{} now has {} dollars".format(self.name, self.money), self.color))
        
        # Free Parking
        FP_values = specials[specials['Name'] == 'FREE PARKING']['Location'].values
        
        if(self.position in FP_values):
            self.money += free_parking
            free_parking = FP_values
            
        # Jail
        if(self.position in specials[specials['Name'] == 'GO TO JAIL']['Location'].values or self.position == -1):
            print(colored("{} is now in jail!".format(self.name), "red"))
            self.position = -1
            self.jail = 0


class Property:
    def __init__(self, name, location, color, rents, prices):
        self.name = name
        self.location = location
        self.color = color
        self.rents = [int(r) for r in rents] 
        self.prices = [int(p) for p in prices] 
        self.owner = None
        self.set = False
        self.houses = 0
        self.mortgaged = False
        
    def add_houses(self, other):
        total_houses = self.houses + other.houses
        self.houses = total_houses
        return self.houses
        
    def get_currentRent(self):
        if(self.owner == None):
            currentRent = 0
        elif(self.set == False):
            currentRent = self.rents[0]
        else:
            currentRent = self.rents[houses+1]
            
        return currentRent
        
        
class Railroad(Property):
    def __init__(self, name, location, rents, prices):
        self.name = name
        self.location = location
        self.rents = [int(r) for r in rents]
        self.prices = prices
        self.owner = None
        self.rr_owned = 0
        self.mortgaged = False
        
    def get_currentRent(self):
        if(self.owner == None):
            currentRent = 0
        else:
            currentRent = self.rents[self.rr_owned]
        
        return currentRent
        
        
class Utility(Property):
    def __init__(self, name, location, rents, prices):
        self.name = name
        self.location = location
        self.rentmult = [int(r) for r in rents]
        self.prices = prices
        self.owner = None
        self.util_owned = 0
        self.mortgaged = False
        
    def get_currentRent(self, dice_roll):
        if(self.owner == None):
            currentRent = 0
        else:
            print("Current rent is {}x a dice roll.".format(self.rentmult[self.util_owned]))
            currentRent = dice_roll * self.rentmult[self.util_owned]