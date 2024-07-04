import json
from urllib.request import urlopen
import requests
import os

# Define the URL for the Steam API endpoint
url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'

# Fetch data from the URL
response = urlopen(url)

# Load JSON data from the response
data = json.load(response)

# Simulating your games_list function
def get_game_list():
    return ["Ghost of Tsushima DIRECTOR'S CUT", "Forza Horizon 5"]

games_list = get_game_list()

# Extract and print the app list
app_list = data['applist']['apps']

for app in app_list:
    for game in games_list:
        if game == app['name']:
            image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app['appid']}/library_600x900_2x.jpg"
            filename = os.path.join('static', 'icon', f"{game}.jpg")
            if not os.path.exists(os.path.join('static', 'icon')):
                os.makedirs(os.path.join('static', 'icon'))
            try:
                # Send a GET request to download the image
                image_response = requests.get(image_url)

                # Check if the request was successful (status code 200)
                if image_response.status_code == 200:
                    # Open a file with the filename to write the image content
                    with open(filename, 'wb') as f:
                        f.write(image_response.content)
                    print(f"Image downloaded successfully as {filename}")
                else:
                    print(f"Failed to download image: HTTP status code {image_response.status_code}")
            except requests.RequestException as e:
                print(f"Failed to download image: {e}")
