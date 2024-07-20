api_key='5b3ce3597851110001cf6248f956e8f938614f9cbf9f13f2fa33c974' #secret hona chahiye

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import os
import json

app = Flask(__name__)
app.secret_key = api_key
DATA_FILE = 'users.json'


def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_users(users):
    with open(DATA_FILE, 'w') as file:
        json.dump(users, file)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], coins=session.get('coins', 0))
    else:
        return redirect(url_for('login'))

def save_users(users):
    with open(DATA_FILE, 'w') as file:
        json.dump(users, file)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['coins'] = users[username]['coins']
            return redirect(url_for('index'))
        elif username not in users:
            users[username] = {'password': password, 'coins': 0, 'selfies': 0}
            save_users(users)
            session['username'] = username
            session['coins'] = users[username]['coins']
            return redirect(url_for('index'))
        else:
            return "Incorrect password", 401
    return render_template('login.html')


@app.route('/upload_selfie', methods=['POST'])
def upload_selfie():
    if 'username' in session:
        username = session['username']
        file = request.files['selfie']
        if file:
            filename = f'selfies/{username}_{len(os.listdir("selfies"))}.jpg'
            file.save(filename)
            users = load_users()
            users[username]['selfies'] += 1
            users[username]['coins'] += 5
            session['coins'] = users[username]['coins']
            save_users(users)
            return jsonify(success=True, location={'latitude': 51.505, 'longitude': -0.09}, coins=users[username]['coins'])
    return jsonify(success=False)


@app.route('/api/route', methods=['POST'])
def get_route():
    data = request.get_json()
    start = data['start']
    end = data['end']
    mode = data['mode']
    # This is a mock response. Replace this with actual route calculation logic.
    return jsonify(routes=[{'duration': 1800, 'distance': 5000}])

@app.route('/users.json')
def users_json():
    # Serve the users.json file
    json_file_path = os.path.join(app.static_folder, 'users.json')
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return jsonify(data)


@app.route('/finish', methods=['POST'])
def finish_trip():
    if 'username' in session:
        username = session['username']
        users = load_users()
        if username in users:
            users[username]['coins'] += 5  # Add 5 coins for completing the trip
            session['coins'] = users[username]['coins']
            save_users(users)
            return jsonify(success=True, coins=users[username]['coins'])
    return jsonify(success=False)

@app.route('/leaderboard')
def leaderboard():
    # Load users data from users.json
    users = load_users()
    
    # Prepare a list of users with their usernames and coin counts
    leaderboard_data = [{'username': username, 'coins': user['coins']} for username, user in users.items()]
    
    # Render the leaderboard.html template with the data
    return render_template('leaderboard.html', leaderboard=leaderboard_data)


if __name__ == '__main__':
    app.run(debug=True)

