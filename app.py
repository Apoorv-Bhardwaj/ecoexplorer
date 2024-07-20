from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/')
def index():
    if 'username' in session:
        users = load_users()
        username = session['username']
        coins = users.get(username, {}).get('coins', 0)
        return render_template('index.html', username=username, coins=coins)
    return redirect(url_for('login'))

@app.route('/upload_selfie', methods=['POST'])
def upload_selfie():
    if 'username' in session:
        username = session['username']
        # Handle file upload and location extraction
        # Update user coins (for example, increment by 10)
        users = load_users()
        if username in users:
            users[username]['coins'] += 10
            save_users(users)
            return jsonify(success=True, location={'latitude': 51.505, 'longitude': -0.09}, coins=users[username]['coins'])
    return jsonify(success=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid credentials', 403
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
