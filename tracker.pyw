import time     # time.sleep()
import psutil   # to check if the .exe is running
from datetime import datetime
import json
from secret import api_key
from steam_web_api import Steam


game_names = ["GhostOfTsushima"]   # List of game executable names (without .exe)


INCREMENT_VAR = 60       # Time increment in seconds, the higher the # the better the performance 

def main():
    # updates game img url, only needed to run once at the start
    # getURLs()
    while True:             
        time.sleep(INCREMENT_VAR)
        # retrives all current running game
        running_games = get_running_games()
        for running_game in running_games:
            # updates the running games playtime
            update_playtime(running_game)
            # updates the running games playtime today
            update_delta_playtime(running_game)
            # updates jsopn file
            update_json(running_game)

# returns a list of running games
def get_running_games():
    running_games = set()
    for process in psutil.process_iter(["name"]):   # gets all processes currently running
        process_name = process.info["name"]
        for game in game_names:                 # gets all games in list
            if process_name == game + ".exe":
                running_games.add(game)
    return running_games


# creates, and updates file with playtime
def update_playtime(running_game):
    # Opens json file
    json_file = open('data.json')

    # converts json file into a dict
    data = json.load(json_file)
    
    playtime = (int(data['Game'][game_names.index(running_game)]['Playtime']) + INCREMENT_VAR)
    return playtime


# creates file holding playtime for the day 
def update_delta_playtime(running_game):
    # current date
    today = datetime.today().strftime('%Y-%m-%d')

    # Opens json file
    json_file = open('data.json')

    # converts json file into a dict
    data = json.load(json_file)

    if not today in data['Game'][game_names.index(running_game)]:
        delta_playtime = 0
        delta_playtime = INCREMENT_VAR + delta_playtime

    else:
        delta_playtime = data['Game'][game_names.index(running_game)][today]
        delta_playtime = INCREMENT_VAR + delta_playtime

    

    return delta_playtime


# gets urls for game img
def getURLs(game):
    steam = Steam(api_key)
    imgURLs = []
    for game in game_names:
        output = steam.apps.search_games(game)
        id = output["apps"][0]["id"][0]
        imgURL = "https://cdn.cloudflare.steamstatic.com/steam/apps/" + str(id) + "/library_600x900_2x.jpg"
        imgURLs.append(imgURL)
    
    return(imgURLs)

# updates json responsable for storing all playtime data
# arguments passes 
def update_json(running_game):
    # Opens json file
    json_file = open('data.json')

    # converts json file into a dict
    data = json.load(json_file)

    index = game_names.index(running_game)

    if not data['Game'][index]['Name']:
        data['Game'][index]['Name'] = running_game
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)

    if not data['Game'][index]['IconURL']:
        data['Game'][index]['IconURL'] = getURLs(running_game)[index]
        with open('data.json', 'w') as file:    
            json.dump(data, file, indent=2)

    
    data['Game'][index]['Playtime'] = update_playtime(running_game)
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

    # current date
    today = datetime.today().strftime('%Y-%m-%d')
    
    data['Game'][index][today] = update_delta_playtime(running_game)
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

main()