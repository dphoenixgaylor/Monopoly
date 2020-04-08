from dependencies import *

def h_portion(players, properties, railroads, utilities, space_list, start, increment, length, position):
    
    end = start + (increment * length)
    SL_initials = space_list['SL_initials']
    SL_price = space_list['SL_price']
    
    if(position == 'top'):
        print('   ', end = '')
        for l in range(start, end, increment):
            positioned = ''
            
            for p in range(len(players)):
                if(players[p].position == l):
                    positioned += colored(players[p].name[0], players[p].color)
                    
            print(positioned + ' ' * (7 - len(positioned)), end = '')
        print('')
                        
    
    print('  ', '─────  ' * length)
    print('  ', end = '')
    
    for i in range(start, end, increment):
        try:
            if(properties[space_list['Name'][i]].owner == None):
                print('|{}*|'.format(SL_initials[i]), end = '')
            else:
                print('│{}{}|'.format(SL_initials[i], properties[space_list['Name'][i]].owner[0]), end = '')
        except KeyError:
            try:
                if(railroads[space_list['Name'][i]].owner == None):
                    print('|{}*|'.format(SL_initials[i]), end = '')
                else:
                    print('│{}{}|'.format(SL_initials[i], railroads[space_list['Name'][i]].owner[0]), end = '')       
            except KeyError:
                try:
                    if(utilities[space_list['Name'][i]].owner == None):
                        print('|{}*|'.format(SL_initials[i]), end = '')
                    else:
                        print('│{}{}|'.format(SL_initials[i], utilities[space_list['Name'][i]].owner[0]), end = '')
                except KeyError:
                    print('|{} |'.format(SL_initials[i]), end = '')

    print('')
    print('  ', end = '')
    
    for p in range(start, end, increment):
        try:
            if(properties[space_list['Name'][p]].owner == None):
                print('|${}{}|'.format(' ' * (4 - len(str(properties[space_list['Name'][p]].prices[0]))), properties[space_list['Name'][p]].prices[0]), end = '')
            else:
                print('|${}{}|'.format(' ' * (4 - len(str(properties[space_list['Name'][p]].get_currentRent()))), properties[space_list['Name'][p]].get_currentRent()), end = '')
        except KeyError:
            try:
                if(railroads[space_list['Name'][p]].owner == None):
                    print('|${}{}|'.format(' ' * (4 - len(str(railroads[space_list['Name'][p]].prices))), railroads[space_list['Name'][p]].prices), end = '')
                else:
                    print('|${}{}|'.format(' ' * (4 - len(str(railroads[space_list['Name'][p]].get_currentRent()))), railroads[space_list['Name'][p]].get_currentRent()), end = '')
            except KeyError:
                try:
                    if(utilities[space_list['Name'][p]].owner == None):
                        print('|${}{}|'.format(' ' * (4 - len(str(utilities[space_list['Name'][p]].prices))), utilities[space_list['Name'][p]].prices), end = '')
                    else:
                        print('|${}{}x|'.format(' ' * (3 - len(str(utilities[space_list['Name'][p]].rentmult)))), utilities[space_list['Name'][p]].rentmult, end = '')
                except KeyError: 
                    print('|{}|'.format(SL_price[p]), end = '')
                    
    print('')
    print('  ', '─────  ' * length)
    
    if(position == 'bottom'):
        print('   ', end = '')
        
        for l in range(start, end, increment):
            positioned = ''

            for p in range(len(players)):
                if(players[p].position == l):
                    positioned += colored(players[p].name[0], players[p].color)

            print(positioned + ' ' * (7 - len(positioned)), end = '')
        print('')
        
        
def v_portion(players, properties, railroads, utilities, space_list, left, right, length, special_row = ''):
    
    SL_initials = space_list['SL_initials']
    SL_price = space_list['SL_price']
    
    if(special_row != 'first'):
        if(special_row == 'last'):
            print('  ', '─────', ' -----', ' ' * (length-2)*6, '   ─────')
        else:
            print('  ', '─────', ' ' * (length-2)*7, '─────')
    
    for i in [left, right]:
        
        play_pos_disp = ''
        play_pos = ''
        
        for player in range(len(players)):
            if(players[player].position == i):
                play_pos_disp += colored(players[player].name[0], players[player].color)
                play_pos += players[player].name[0]
            
        skip = False
        
        if(i == left):
            play_pos_disp += ' ' * (2 - len(play_pos))
            if(len(play_pos) > 2):
                print(play_pos_disp[:20], end = '')
            else:
                print(play_pos_disp, end = '')
            
        try:
            if(properties[space_list['Name'][i]].owner == None):
                print('|{}*|'.format(SL_initials[i]), end = '')
            else:
                print('│{}{}|'.format(SL_initials[i], properties[space_list['Name'][i]].owner[0]), end = '')
        except KeyError:
            try:
                if(railroads[space_list['Name'][i]].owner == None):
                    print('|{}*|'.format(SL_initials[i]), end = '')
                else:
                    print('│{}{}|'.format(SL_initials[i], railroads[space_list['Name'][i]].owner[0]), end = '')       
            except KeyError:
                try:
                    if(utilities[space_list['Name'][i]].owner == None):
                        print('|{}*|'.format(SL_initials[i]), end = '')
                    else:
                        print('│{}{}|'.format(SL_initials[i], utilities[space_list['Name'][i]].owner[0]), end = '')
                except KeyError:
                    try:
                        print('|{} |'.format(SL_initials[i]), end = '')
                    except IndexError:
                        print('    . ', end = '')
                        skip = True
                        
        if(i == right):
            if(skip == True):
                print(' ')
            else:
                if(len(play_pos) < 2):
                    print(' ', end = '')
                    print(play_pos_disp)
                elif(len(play_pos) > 2):
                    print(play_pos_disp[:20])
        
        elif(i == left and special_row == 'last'):
            print('¦JAIL:¦', ' ' * (length-2)*6, end = ' ')
        else:
            print(' ' * (length-2)*7, end = '')
    

    for p in [left, right]:
        
        play_pos_disp = ''
        play_pos = ''
        
        for player in range(len(players)):
            if(players[player].position == p):
                play_pos_disp += colored(players[player].name[0], players[player].color)
                play_pos += players[player].name[0]
            
        skip = False
        
        if(p == left):
            if(len(play_pos) > 2):
                print('+{}'.format(len(play_pos) - 2), end = '')
            else:
                print('  ', end = '')
            
        
        try:
            if(properties[space_list['Name'][p]].owner == None):
                print('|${}{}|'.format(' ' * (4 - len(str(properties[space_list['Name'][p]].prices[0]))), properties[space_list['Name'][p]].prices[0]), end = '')
            else:
                print('|${}{}|'.format(' ' * (4 - len(str(properties[space_list['Name'][p]].get_currentRent()))), properties[space_list['Name'][p]].get_currentRent()), end = '')
        except KeyError:
            try:
                if(railroads[space_list['Name'][p]].owner == None):
                    print('|${}{}|'.format(' ' * (4 - len(str(railroads[space_list['Name'][p]].prices))), railroads[space_list['Name'][p]].prices), end = '')
                else:
                    print('|${}{}|'.format(' ' * (4 - len(str(railroads[space_list['Name'][p]].get_currentRent()))), railroads[space_list['Name'][p]].get_currentRent()), end = '')
            except KeyError:
                try:
                    if(utilities[space_list['Name'][p]].owner == None):
                        print('|${}{}|'.format(' ' * (4 - len(str(utilities[space_list['Name'][p]].prices))), utilities[space_list['Name'][p]].prices), end = '')
                    else:
                        print('|${}{}x|'.format(' ' * (3 - len(str(utilities[space_list['Name'][p]].rentmult)))), utilities[space_list['Name'][p]].rentmult, end = '')
                except KeyError: 
                    try:
                        print('|{}|'.format(SL_price[p]), end = '') 
                    except IndexError:
                        print('    . ', end = '')
                        skip = True
                      
        if(p == right):
            if(skip == True):
                print(' ', end = '')
            elif(len(play_pos) > 2):
                print('+{}'.format(len(play_pos) - 2), end = '')                
        
        elif(p == left and special_row == 'last'):
            prisoners = ''
            count = 0

            for p in range(len(players)):
                if(players[p].position == -1):
                    prisoners += colored(players[p].name[0], players[p].color)
                    count += 1

            prisoners += ' ' * (5-count)
            
            print('¦{}¦'.format(prisoners), ' ' * (length-2)*6, end = ' ')
            
        else:
            print(' ' * (length-2)*7, end = '')
                    
    print('')
    
    

