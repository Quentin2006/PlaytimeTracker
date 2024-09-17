import time     # time.sleep()
import psutil   # to check if the .exe is running
from datetime import datetime
import json
from secret import api_key
from steam_web_api import Steam
import re
import os

INCREMENT_VAR = 1       # Time increment in seconds, the higher the # the better the performance 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data.json')






def getExeNames():
    # Load the JSON data from the file
    with open(DATA_FILE_PATH, 'r') as file:
        data = json.load(file)

    # Initialize an empty list to store game names
    game_names = []

    # Iterate through each game in the JSON data and add the game name to the list
    for game in data['Game']:
        game_names.append(game['ExeName'])

    return game_names






def main():
    global game_names
    # updates game img url, only needed to run once at the start

    while True:
        time.sleep(INCREMENT_VAR)

        game_names = getExeNames()

        UpdateJsonEntry(game_names)
        
        # only used to update games taht a running
        for running_game in get_running_games():
            # checks if json game data is there
            updatePlaytime(running_game)







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
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)
    
    playtime = (int(data['Game'][game_names.index(running_game)]['Playtime']) + INCREMENT_VAR)
    return playtime






# creates file holding playtime for the day 
def update_delta_playtime(running_game):
    # current date
    today = datetime.today().strftime('%Y-%m-%d')

    # Opens json file
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)

    if not today in data['Game'][game_names.index(running_game)]:
        delta_playtime = 0
        delta_playtime = INCREMENT_VAR + delta_playtime

    else:
        delta_playtime = data['Game'][game_names.index(running_game)][today]
        delta_playtime = INCREMENT_VAR + delta_playtime

    

    return delta_playtime



# input game name, returns object of game info
# {'id': arr of int, 'link': str, 'name': str, 'img': str, 'price': str}
def getGameSteamGameInfo(game):
    steam = Steam(api_key)
    # tries defalt exe name
    try:
        output = steam.apps.search_games(game)
        id = output["apps"][0]
        return id

    # handles IndexError (empty list)
    except IndexError:
        print("IndexError occurred with default name.")  # Log for debugging

        # adds spaces after every capital letter
        newString = re.sub(r'(?<!^)(?=[A-Z])', ' ', game)
        try:
            output = steam.apps.search_games(newString)
            id = output["apps"][0]  # Potential IndexError or KeyError
            return id
        except IndexError:
            print("IndexError occurred again after modifying game name.")
            return "None"



# Returns format to find steam url using SteamGridDB.com
def getURLs(game):

    if getGameSteamGameInfo(game) != "None":
        imgURL = "https://cdn.cloudflare.steamstatic.com/steam/apps/" + str(getGameSteamGameInfo(game)["id"][0]) + "/library_600x900_2x.jpg"
        return imgURL
    
    else: return getGameSteamGameInfo(game)



# Returns Game name according to steam
def getGameName(game):
    
    if getGameSteamGameInfo(game) != "None":
        return getGameSteamGameInfo(game)["name"]
    
    else: return getGameSteamGameInfo(game)



# updates json playtime data
def updatePlaytime(game):
    # Opens json file
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)

    index = game_names.index(game)
    
    data['Game'][index]['Playtime'] = update_playtime(game)
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    # current date
    today = datetime.today().strftime('%Y-%m-%d')
    
    data['Game'][index][today] = update_delta_playtime(game)
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)


# if there is no json in file, 
def UpdateJsonEntry(gameNames):
    # Opens json file
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)

    index = 0
    for game in gameNames:
        
        # no need to check for name, its allways given

        if 'RealName' not in data['Game'][index]:
            data['Game'][index]['RealName'] = getGameName(game)

            with open(DATA_FILE_PATH, 'w') as file:    
                json.dump(data, file, indent=2)

        if 'IconURL' not in data['Game'][index]:
            data['Game'][index]['IconURL'] = getURLs(game)

            with open(DATA_FILE_PATH, 'w') as file:    
                json.dump(data, file, indent=2)
        
        if 'Playtime' not in data['Game'][index]:
            data['Game'][index]['Playtime'] = 0

            with open(DATA_FILE_PATH, 'w') as file:    
                json.dump(data, file, indent=2)

        index += 1


main()