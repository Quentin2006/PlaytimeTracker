import time     # time.sleep()
import psutil   # to check if the .exe is running
import os
from datetime import datetime, timedelta

game_names = ["GhostOfTsushima", "ForzaHorizon5"]   # List of game executable names (without .exe)

tracked_files = {game: f"{game}.txt" for game in game_names}

increment_var = 60       # Time increment in seconds, the higher the # the better the performance 

def main():
    while True:             
        time.sleep(increment_var)
        running_games = get_running_games()
        for game in running_games:
            update_playtime(game)
            update_delta_playtime(game)
            print(f"{game} is running")

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
def update_playtime(game):
    # Correct file path construction
    file_name = os.path.join('playtimes', tracked_files[game])

    # if folder doesn't exist, folder is made
    if not os.path.exists('playtimes'):
        os.makedirs('playtimes')
    
    # if file does not exist, it will create file and start at 0
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write('0')

    # opens file in read mode to get contents of file
    with open(file_name, 'r') as file:
        content = int(file.read().strip())
        playtime = content + increment_var

    # opens file in write mode to update play time
    with open(file_name, 'w') as file:
        file.write(str(playtime))
    return playtime

# creates file holding playtime for the day 
def update_delta_playtime(game):
    # current date
    today = datetime.today().strftime('%Y-%m-%d')

    # Correct file path construction for today playtime
    file_name = os.path.join('playtimes', 'delta_playtime', f"{game}_{today}.txt")

    # if folder doesn't exist, folder is made
    if not os.path.exists(os.path.join('playtimes', 'delta_playtime')):
        os.makedirs(os.path.join('playtimes', 'delta_playtime'))
        
    # if file does not exist, it will create file and start at 0
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write('0')

    # opens file in read mode to get contents of file
    with open(file_name, 'r') as file:
        content = int(file.read().strip())
        delta_playtime = content + increment_var

    # opens file in write mode to update play time
    with open(file_name, 'w') as file:
        file.write(str(delta_playtime))
    return delta_playtime

# used to retrieve game_names
def get_game_list():
    return game_names

# used to retrieve game_names
def get_playtime_list():
    game_playtimes = []
    for game in game_names:
        file_name = os.path.join('playtimes', game + '.txt')
        # opens file in read mode to get contents of file
        with open(file_name, 'r') as file:
            content = int(file.read().strip())
            game_playtimes.append(content)
    return game_playtimes

def get_delta_playtime_list():
    today = datetime.today().strftime('%Y-%m-%d')

    game_delta_playtime = []
    
    for game in game_names:
        file_name = os.path.join('playtimes', 'delta_playtime', f"{game}_{today}.txt")
        # Check if the file exists before trying to read it
        if os.path.exists(file_name):
            # opens file in read mode to get contents of file
            with open(file_name, 'r') as file:
                content = int(file.read().strip())
                game_delta_playtime.append(content)

    return game_delta_playtime

def rfind(lst, element, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(lst)
    for i in range(end-1, start-1, -1):
        if lst[i] == element:
            return i
    return -1

# WOW I AM STRUGGLING
def get_last_played_list():
    folder_path = "./playtimes/delta_playtime"
    filenames = os.listdir(folder_path)

    game_date = []
    today_date = datetime.today()

    for game in game_names:
        found = False
        i = 0
        while not found and i < 365:  # Limit to checking up to 365 days ago
            date = today_date - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            filename_to_check = f"{game}_{date_str}.txt"

            if filename_to_check in filenames:
                game_date.append(filename_to_check)
                found = True            
            i += 1


    game_date = [filename.split('_')[1].split('.')[0] for filename in game_date]

    return game_date







get_last_played_list()