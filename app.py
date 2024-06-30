from flask import Flask, render_template
from tracker import main
import threading

app = Flask(__name__)

@app.route('/')
def index():

    game_name = 'GhostOfTsushima'
    file_name = game_name + '.txt'

    # opens file in read mode to get contents of file
    with open(file_name, 'r') as file:
        content = int(file.read().strip())
        playtime = content

    return render_template('index.html', game_name=game_name, game_playtime=playtime)

if __name__ == "__main__":
    # Start main in a separate thread
    main_thread = threading.Thread(target=main)
    main_thread.start()

    # Run the Flask app
    app.run(debug=True)
    
