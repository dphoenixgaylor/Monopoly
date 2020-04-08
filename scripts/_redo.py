

        
    def jailed(self):
        print(self.name, "is currently in jail. Which would you like to do?")
        print("> Try to roll a double -- [Type: D]")
        
        if(self.money >= 50):
            print("> Pay $50 -- [Type: P]")
        else:
            print(self.name, "> Pay $50 -- Unfortunately, ", self.name, "does not have enough money to bail out of jail.")
        
        if(self.cards[0] == True):
            print("> Use your get out of jail free card (Chance) -- [Type: CH]")
        if(self.cards[1] == True):
            print("> Use your get out of jail free card (Community Chest) -- [Type: CC]")
            
        response = input("Choice: ").upper()
        
        if(response == 'D'):
            x = random.randrange(1,7)
            y = random.randrange(1,7)
           
            print(self.name, "rolled a", x, "and a", y)
                  
            if(x == y):
                print("Congratulations!", self.name, "moves", x + y, "spaces.")
    
            else:
                print("Unfortunately,", self.name, "did not roll a double.")
                self.jail = self.jail + 1
                  
                if(self.jail == 3):
                    self.money -= 50
                    
                    if(self.money < 0):
                        no_money()
                    
                    else:    
                        print("Because this is the 3rd failed attempt to roll a double,", self.name, 
                              "pays $50 and is freed.")
                        
                        self.position = 10 + total
                        self.jail = -1
                        
                return None
            
            self.position = 10 + total
            
        if(response == 'P'):
            if(self.money >= 50):
                self.money -= 50
                print(self.name, "pays $50 and is freed from jail.", self.name, "now has", self.money, "dollars.")
                self.jail = -1
                self.position = 10
                move_position()
                
            else:
                print("Unfortunately,", self.name, "has less than $50 and cannot bail out of jail.")
                jailed()
                
        if(response == 'CH'):
            if(self.cards[0] == True):
                self.cards[0] = False
                print(self.name, "uses a GET OUT OF JAIL FREE card and is bailed out of jail.")
                self.jail = -1
                self.position = 10
                move_position()
                
            else:
                print("Unfortunately,", self.name, "does not have a CHANCE card for getting out of jail.")
                jailed()
                
        if(response == 'CC'):
            if(self.cards[1] == True):
                self.cards[1] = False
                print(self.name, "uses a GET OUT OF JAIL FREE card and is bailed out of jail.")
                self.jail = -1
                self.position = 10
                move_position()
                
            else:
                print("Unfortunately,", self.name, "does not have a COMMUNITY CHEST card for getting out of jail.")
                jailed()
        
        else:
            print("Invalid option!")
            jailed()
               
    def no_money(self):
        print("Oh no!", self.name, "has fallen under $0.")
            
        if((self.properties == []) and (True not in self.cards)):
            print(self.name, "has no properties to mortage or sell.")
            print(self.name, "does not have any GET OUT OF JAIL FREE cards to sell.")
            print(self.name, "has lost the game.")
                    
            global players
            players.remove(self)
                
            if(len(players) == 1):
                print(players[0], "has won the game!! Congratulations!!")
                game_over()
                    
        else:
            print("Which would you like to do?")
                
            if(self.properties != []):
                print("> Mortage a property -- [Type: M]")
                print("> Sell a property -- [Type: S]")
                          
            if(self.cards[0] == True):
                print("> Sell get out of jail free card (CHANCE) -- [Type: CH]")
                
            if(self.cards[1] == True):
                print("> Sell get out of jail free card (COMMUNITY CHEST) -- [Type: CC]")                    
            
            response = input("Choice: ").upper()
                          
            if(response == 'M'):
                if(self.properties == []):
                    print("Unfortunately,", self.name, "has no properties to mortgage.")
                    no_money()
                        
                for prop in self.properties:
                    if(properties[prop].mortgaged == False):
                        print(prop, "- Mortage Value:", properties[prop].prices[0]/2, "-- Type:", properties[prop].location)
                            
                        if(properties[prop].houses > 0):
                            print("For this property, you also have", properties[prop].houses%5, "houses and",
                                    floor(properties[prop].houses)/5, "hotels that can be sold to the bank for",
                                    properties[prop].prices[1], "each.\n")
                    
                print("Go back. -- Type G")
                    
                pass