import json
from tracker import game_names, get_playtime_list
from game_icon import getURLs

gameInfo = {"game": []}
i = 0
for game in game_names:
    newInfo = {
            "Name": game_names[i],
            "IconURL": getURLs()[i],
            "Playtime": get_playtime_list()[i]
    }
    gameInfo["game"].append(newInfo) 
    i += 1

# Serializing json
json_object = json.dumps(gameInfo, indent=2)
 
# Writing to sample.json
with open("data.json", "w") as outfile:
    outfile.write(json_object)
