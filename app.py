from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data-json', methods = ['GET'])
def GetJSON():
    with open('./data.json') as f:
        return json.load(f)


@app.route('/update-json', methods=['POST'])
def update_json():
    new_data = request.json
    with open('./data.json', 'w') as file:  # 'w' mode to overwrite
        json.dump(new_data, file, indent=4)

    return jsonify(new_data)  # Return the new data as a response

        
if __name__ == "__main__":
    app.run(debug=True)