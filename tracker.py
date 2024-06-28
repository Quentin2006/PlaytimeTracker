import time     # time.sleep()
import psutil   # to check if the .exe is running

exe_names = ["GhostOfTsushima.exe", ]   # holds list of exe names, needs to be manual added every time

for process in psutil.process_iter(['name']):
    for exe in exe_names: 
        if process.info['name'] == exe_names:
