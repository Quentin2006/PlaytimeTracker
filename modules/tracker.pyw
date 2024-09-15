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


def getGameNames():
    # Load the JSON data from the file
    with open(DATA_FILE_PATH, 'r') as file:
        data = json.load(file)

    # Initialize an empty list to store game names
    game_names = []

    # Iterate through each game in the JSON data and add the game name to the list
    for game in data['Game']:
        game_names.append(game['Name'])

    return game_names


game_names = getGameNames()

def main():
    global game_names
    # updates game img url, only needed to run once at the start
    while True:
        time.sleep(INCREMENT_VAR)
        game_names = getGameNames()
        # checks if game img is there, if not, it updates it
        update_game_img(game_names)
        # retrives all current running game
        running_games = get_running_games()
        for running_game in running_games:
            # checks if json game data is there
            create_json(running_game)

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


# gets urls for game img
def getURLs(game):
    steam = Steam(api_key)
    try:
        output = steam.apps.search_games(game)
        id = output["apps"][0]["id"][0]
        print(id)
        imgURL = "https://cdn.cloudflare.steamstatic.com/steam/apps/" + str(id) + "/library_600x900_2x.jpg"
        return imgURL

    except IndexError:
        newString = re.sub(r'(?<!^)(?=[A-Z])', ' ', game)
        output = steam.apps.search_games(newString)
        id = output["apps"][0]["id"][0]
        print(id)
        imgURL = "https://cdn.cloudflare.steamstatic.com/steam/apps/" + str(id) + "/library_600x900_2x.jpg"
        return imgURL
    except:
        return "None"

    

# updates json responsable for storing all playtime data
def update_json(running_game):
    # Opens json file
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)

    index = game_names.index(running_game)
    
    data['Game'][index]['Playtime'] = update_playtime(running_game)
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

    # current date
    today = datetime.today().strftime('%Y-%m-%d')
    
    data['Game'][index][today] = update_delta_playtime(running_game)
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

def update_game_img(game_names):
    # Opens json file
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)

    for game in game_names:

        index = game_names.index(game)

        if data['Game'][index]['IconURL'] == "":
            data['Game'][index]['IconURL'] = getURLs(game)

            with open(DATA_FILE_PATH, 'w') as file:    
                json.dump(data, file, indent=2)
    
# if there is no json in file then it makes json entry for game
def create_json(running_game):
    # Opens json file
    json_file = open(DATA_FILE_PATH)

    # converts json file into a dict
    data = json.load(json_file)

    index = game_names.index(running_game)

    if index >= len(data['Game']):
        newData = {
            "Name": running_game,
            "IconURL": "",
            "Playtime": 0
        }
        data['Game'].append(newData)
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

main()