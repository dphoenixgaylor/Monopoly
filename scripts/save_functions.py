from dependencies import *

def save_properties(properties, property_names):
    p0_details = properties[property_names[0]].__dict__
    property_details = []

    for prop in range(len(property_names)):
        details = properties[property_names[prop]].__dict__
        property_details.append(details.values())

    property_details = pd.DataFrame(property_details, columns = p0_details.keys())
    property_details['property_names'] = property_names

    return property_details


def save_railroads(railroads, railroad_names):
    r0_details = railroads[railroad_names[0]].__dict__
    railroad_details = []

    for rail in range(len(railroad_names)):
        details = railroads[railroad_names[rail]].__dict__
        railroad_details.append(details.values())

    railroad_details = pd.DataFrame(railroad_details, columns = r0_details.keys())
    railroad_details['railroad_names'] = railroad_names

    return railroad_details


def save_utilities(utilities, utility_names):
    u0_details = utilities[utility_names[0]].__dict__
    utility_details = []

    for util in range(len(utility_names)):
        details = utilities[utility_names[util]].__dict__
        utility_details.append(details.values())

    utility_details = pd.DataFrame(utility_details, columns = u0_details.keys())
    utility_details['utility_names'] = utility_names

    return utility_details

def save_players(players):
    p0_details = players[0].__dict__
    player_details = [p0_details.values()]

    for play in range(1, len(players)):
        details = players[play].__dict__
        player_details.append(details.values())

    player_details = pd.DataFrame(player_details, columns = p0_details.keys())

    return player_details