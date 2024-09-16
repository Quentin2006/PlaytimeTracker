import pystray
import PIL.Image
import webview
import os
import sys
from threading import Thread, Event

# Get the parent directory of the 'modules' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, 'modules')

# Add the 'modules' directory to sys.path
sys.path.append(MODULES_DIR)


from app import app


stop_event = Event()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_FILE_PATH = os.path.join(BASE_DIR, 'modules/static/icon.png')

image = PIL.Image.open(IMG_FILE_PATH)

host = "http://127.0.0.1"
port = 5000    

def run():
    while not stop_event.is_set():
        app.run(port=port, use_reloader=False)

def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
    elif str(item) == "Open":
        webview.create_window('Playtime Tracker', f"{host}:{port}", width=1600, height=900, background_color='#000000', shadow=True)
        webview.start()

icon = pystray.Icon("Playtime Tracker", image, menu=pystray.Menu(
    pystray.MenuItem("Open", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))

if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True
    t.start()

    icon.run()

    stop_event.set()
