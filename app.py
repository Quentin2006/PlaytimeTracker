from flask import Flask, render_template, jsonify, request
from tracker import get_playtime_list, get_game_list, get_delta_playtime_list, get_last_played_list, main
import threading
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_info')
def fetch_game_info():
    game_list = get_game_list()
    playtime_list = get_playtime_list()
    delta_playtime_list = get_delta_playtime_list()
    last_played_list = get_last_played_list()

    game_info = []

    i=0
    for i in range(len(game_list)):
        game_info.append({
                    "name": game_list[i],
                    "playtime": playtime_list[i] if i < len(playtime_list) else "N/A",
                    "recent_playtime": delta_playtime_list[i] if i < len(delta_playtime_list) else "N/A",
                    "last_played": last_played_list[i]
                })
    return jsonify({"games": game_info})



if __name__ == '__main__':
    # Check if running in the main process to avoid running the thread multiple times
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        tracking_thread = threading.Thread(target=main)
        tracking_thread.daemon = True
        tracking_thread.start()
    
    app.run(debug=True)
    
