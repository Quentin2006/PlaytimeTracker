import pystray
import PIL.Image
from app import main

image = PIL.Image.open("clock.webp")

def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
    elif str(item) == "Open":
        main()

icon = pystray.Icon("Playtime Tracker", image, menu=pystray.Menu(
    pystray.MenuItem("Open", main),
    pystray.MenuItem("Exit", on_clicked)
))

icon.run()
