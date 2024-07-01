import time     # time.sleep()
import psutil   # to check if the .exe is running
import os

game_names = ["GhostOfTsushima", "ForzaHorizon5", "Apex", "Minecraft"]   # List of game executable names (without .exe)

tracked_files = {game: f"{game}.txt" for game in game_names}

increment_var = 1       # Time increment in seconds, the higher the # the better the performance 

def main():
    while True:             
        time.sleep(increment_var)
        running_games = get_running_games()
        for game in running_games:
            update_playtime(game)
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

# used to retrieve game_names
def get_game_list():
    return game_names

# used to retrieve game_names
def get_playtime_list():
    game_playtimes = []
    for game in game_names:
        file_name = "./playtimes/" + game + ".txt"
        # opens file in read mode to get contents of file
        with open(file_name, 'r') as file:
            content = int(file.read().strip())
            game_playtimes.append(content)
    return game_playtimes

game_playtimes = get_playtime_list()

print(game_playtimes)