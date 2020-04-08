from dependencies import *

ownable_names = property_names + railroad_names + utility_names
all_names = ownable_names + special_names
all_locs = np.concatenate([property_locations, railroad_locations, utility_locations, special_locations])

space_list = pd.DataFrame(all_names, all_locs, columns = ['Name'])
space_list = space_list.sort_index()

fail = False

for i in range(len(space_list.index)-1):

    if(dev == True):
        if(space_list.index[i+1] - space_list.index[i] > 1):
            print(colored(
                "Warning: There is empty space between spaces %s and %d. Consider giving a name in special_locations.\n" \
                  %(space_list.index[i], space_list.index[i+1]), "yellow"))

    if(space_list.index[i+1] - space_list.index[i] == 0):
        if(dev == True):
            fail = True
            print(colored(
                "ERROR: You may NOT use the same location multiple times. Please correct the issue with location number %s." \
                  %(space_list.index[i]), "red"))

        else:
            print(colored(
                "This game cannot be created because some location numbers have been duplicated. Please correct the issue or load a new game.", "red"))
            sys.exit()

duplicates = set([o for o in ownable_names if ownable_names.count(o) > 1])

if(len(duplicates) > 0):
    if(dev == True):
        fail = True
        print(colored(
            "ERROR: You may NOT use duplicate names for properties, railroads, or utilities. Please correct the issue with the following:", "red"))
        print(duplicates)

    else:
        print(colored(
            "This game cannot be created because there are duplicate names for either properties, railroads, or utilities:", "red"))
        print(colored(
            "Please correct the issue or load a new game.", "red"))
        print(duplicates)
        sys.exit()

if(dev == True):
    if(fail == False):
        print(colored("SUCCESS! This game will load properly.\nMore developer functionality coming soon!", "green"))
    else:
        print(colored("\nNOTE: THIS GAME WILL NOT LOAD BECAUSE OF THE ERROR(S) IN RED ABOVE!\n", "red"))
        
space_list = space_list.reindex(range(space_list.index[-1]+1), fill_value = '')

SL_initials = [''] * (len(range(space_list.index[-1])) + 1)
SL_price = [''] * (len(range(space_list.index[-1])) + 1)

for s in space_list.index:
    if(space_list['Name'][s] == 'GO'):
        SL_initials[s] ='GO  '
        
        go_money = int(specials[specials['Location'] == s]['MoneyEarned'].values[0])
        if(go_money >= 1000):
            go_money = str(int(go_money/1000)) + 'K'
        go_money = str(go_money)
        
        SL_price[s] = '+$' + ' ' * (3 - len(go_money)) + go_money
        
    elif(space_list['Name'][s] == 'COMMUNITY'):
        SL_initials[s] = 'COM '
        SL_price[s] = 'CHEST'
        
    elif(space_list['Name'][s] == 'CHANCE'):
        SL_initials[s] = 'CH  '
        SL_price[s] = 'CARD '

    elif(space_list['Name'][s] == 'INCOME TAX'):
        SL_initials[s] = 'TAX '      
        SL_price[s] = ' ' * (4 - len(str(other_parameters['income_tax_rate']))) + str(other_parameters['income_tax_rate']) + '%'
        
    elif(space_list['Name'][s] == 'JUST VISITING'):
        SL_initials[s] = 'JUST'
        SL_price[s] = 'VISIT'
        
    elif(space_list['Name'][s] == 'FREE PARKING'):
        SL_initials[s] = 'FR P'
        
        total_FP = int(free_parking + specials[specials['Location'] == s]['MoneyEarned'].values[0])
        if(total_FP >= 1000):
            total_FP = str(int(total_FP/1000)) + 'K'
        
        SL_price_FP = str(total_FP)
        SL_price[s] = '+$' + ' ' * (3 - len(SL_price_FP)) + SL_price_FP
        
    elif(space_list['Name'][s] == 'GO TO JAIL'):
        SL_initials[s] = 'GOTO'
        SL_price[s] = 'JAIL '
        
    elif(space_list['Name'][s] in specials['Name'].values):
        if('Tax' in space_list['Name'][s]):
            SL_initials[s] = 'TAX '
        
        else:
            letters = ""
            words = space_list['Name'][s].split()
            for word in words:
                letters = letters + word[0]
            letters = letters[:3]
            
            SL_initials[s] = "".join(letters).upper() + ' ' * (4 - len(letters))
        
        money_earned = specials[specials['Location'] == s]['MoneyEarned'].values[0]
        set_position = str(specials[specials['Location'] == s]['SetPosition'].values[0])
        
        if(not math.isnan(money_earned)):
            money_earned = int(money_earned)
            
            if(money_earned >= 1000):
                money_earned_str = str(int(money_earned/1000)) + 'K'
        
        if(money_earned > 0):
            SL_price[s] = '+$' + ' ' * (3 - len(money_earned_str)) + money_earned_str
        elif(money_earned < 0):
            SL_price[s] = '$' + ' ' * (5 - len(str(money_earned))) + str(money_earned)[1:]
        elif('B' in set_position):
            SL_price[s] = 'BACK '
        elif('B' not in set_position):
            SL_price[s] = 'MOVE '
        else:
            SL_price[s] = '     '
    
    else:
        if(space_list['Name'][s] == ''):
            SL_initials[s] = '    '
            SL_price[s] = '     '
        
        else:
            letters = ""
            words = space_list['Name'][s].split()
            for word in words:
                letters = letters + word[0]
                letters = letters[:3]

            SL_initials[s] = "".join(letters).upper() + ' ' * (4 - len(letters))
            SL_price[s] = '*PROP'
        
space_list['SL_initials'] = [initial for initial in SL_initials if initial != '']
space_list['SL_price'] = [price for price in SL_price if price != '']