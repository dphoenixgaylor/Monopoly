from dependencies import *
import save_functions as SF

if(quit == True):
    print("\n")
    print("Would you like to save the game? Type [Y] to save.")
    response = input().upper()
    
    if(response.startswith('Y')):
        print(colored("\nSaving...", "green"))
        
    else:
        print(colored("You have selected to NOT save. Hit enter to continue or type anything to save.", "red"))
        response = input().upper()
              
        if(response == ''):  
            print(colored("Thanks for playing! Exiting game...", "green"))
            sys.exit()
                  
        else:
            print(colored("\nSaving...", "green"))
                   
current_time = datetime.now().strftime("%Y%m%d-%H%M")
current_wd = os.getcwd()

if(autosave == False):
    print("Please enter a name for your game.")
    save_description = input("Name: ")

else:
    save_description = 'AUTOSAVE'

try:    
    save_directory = current_wd + '\\saves\\' + current_time + '_' + save_description.upper()
    os.mkdir(save_directory) 
except FileExistsError:
    shutil.rmtree(save_directory)
    os.mkdir(save_directory) 
    

fail = False

try:
    SF.save_properties(properties = properties, property_names = property_names).to_csv(save_directory + '\\properties.csv')
    SF.save_railroads(railroads = railroads, railroad_names = railroad_names).to_csv(save_directory + '\\railroads.csv')
    SF.save_utilities(utilities = utilities, utility_names = utility_names).to_csv(save_directory + '\\utilities.csv')
    
    SF.save_players(players = players).to_csv(save_directory + '\\players.csv')
    
    space_list.to_csv(save_directory + '\\space_list.csv')
    chance_deck.to_csv(save_directory + '\\chance_deck.csv')
    community_deck.to_csv(save_directory + '\\community_deck.csv')
    
    pd.DataFrame(chance_cards).to_csv(save_directory + '\\chance_cards.csv')
    pd.DataFrame(community_cards).to_csv(save_directory + '\\community_cards.csv')
    pd.DataFrame([free_parking]).to_csv(save_directory + '\\free_parking.csv')
    
except:
    if(autosave == False):
        print(colored("Unfortunately, something went wrong when saving. Your game was not saved.".format(type), "red"))
        shutil.rmtree(save_directory)
        exec(open("scripts\\player_turn.py").read())
    else:
        print(colored("Autosave has failed. Please note that this means you will not be able to save this current game.", "red"))

else:
    if(autosave == False):
        print(colored("\nYour game has saved successfully!", "green"))

if(quit == False):
    exec(open("scripts\\player_turn.py").read())
else:
    print(colored("See you next time!!", "green"))