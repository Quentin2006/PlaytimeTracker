import time     # time.sleep()
import psutil   # to check if the .exe is running
import os

game_names = ["GhostOfTsushima", "Hades"]   # List of game executable names (without .exe)

tracked_files = {game: f"{game}.txt" for game in game_names}

increment_var = 10   # Time increment in seconds, the higher the # the better the performance 

def main():
    while True:
        time.sleep(increment_var)
        running_games = get_running_games()
        for game in running_games:
            update_playtime(game)
            print(f"{game} is running")

def get_running_games():
    running_games = set()
    for process in psutil.process_iter(["name"]):   # gets all processes currently running
        process_name = process.info["name"]
        for game in game_names:                 # gets all games in list
            if process_name == game + ".exe":
                running_games.add(game)
    return running_games


def update_playtime(game):
    file_name = tracked_files[game]
    
    # if file does not exist, it will create file and start timer at designated increment variable defined above
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write(str(0))

    # opens file in read mode to get contents of file
    with open(file_name, 'r') as file:
        content = int(file.read().strip())
        playtime = content + increment_var

    # opens file in write mode to update play time
    with open(file_name, 'w') as file:
        file.write(str(playtime))

if __name__ == "__main__":
    main()