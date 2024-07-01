from flask import Flask, render_template, jsonify
from tracker import get_playtime_list, get_game_list, main
import threading
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/get_game_list')
def fetch_game_list():
    game_list = get_game_list()
    return jsonify({'games': game_list})

@app.route('/get_playtime_list')
def fetch_playtime_list():
    playtime_list = get_playtime_list()
    return jsonify({'playtimes': playtime_list})

if __name__ == '__main__':
    # Check if running in the main process to avoid running the thread multiple times
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        tracking_thread = threading.Thread(target=main)
        tracking_thread.daemon = True
        tracking_thread.start()
    
    app.run(debug=True)
    
