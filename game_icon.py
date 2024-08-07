from steam_web_api import Steam
from tracker import game_names
from secret import api_key

def getURLs():
    URL = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    steam = Steam(api_key)

    imgURLs = []
    for game in game_names:
        output = steam.apps.search_games(game)
        id = output["apps"][0]["id"][0]
        imgURL = "https://cdn.cloudflare.steamstatic.com/steam/apps/" + str(id) + "/library_600x900_2x.jpg"
        imgURLs.append(imgURL)

    return(imgURLs)

                
