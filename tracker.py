import time     # time.sleep()
import psutil   # to check if the .exe is running
import os

# CURRENTLY ONLY WORKS FOR ONE GAME, WILL MAKE IT WORK FOR MORE 

game_names = ["GhostOfTsushima"]   # MUST BE NAME OF EXE - THE .exe EXTENSION

increment_var = 10   # decides how much program should count by, lower numbers result in better performance

def main():
    while True:
        time.sleep(increment_var)
        for process in psutil.process_iter(["name"]):   # gets all processes currently running
            for game in game_names:                     # gets all games in list
                if process.info["name"] == game + ".exe":
                    create_and_write_to_file(game)          # makes file and tracks playtime
                    print("running")


def create_and_write_to_file(game):
    file_name = game + ".txt"

    # if file does not exist, it will create file and start timer at designated increment variable defined above
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write(str(increment_var))

    # opens file in read mode to get contents of file
    with open(file_name, 'r') as file:
        content = file.read()

    time = int(content) + increment_var

    # opens file in write mode to update play time
    with open(file_name, 'w') as file:
        file.write(str(time))

    return None

main()