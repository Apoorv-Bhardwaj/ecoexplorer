from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_key='5b3ce3597851110001cf6248f956e8f938614f9cbf9f13f2fa33c974' #secret hona chahiye

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/route', methods=['POST'])
def route():
    data = request.json
    start_coords = data['start']
    end_coords = data['end']
    mode = data['mode']
    url = f'https://api.openrouteservice.org/v2/directions/{mode}'
    params = {
        'api_key': api_key,
        'start': f'{start_coords[1]},{start_coords[0]}',
        'end': f'{end_coords[1]},{end_coords[0]}'
    }

    response = requests.get(url, params=params)
    route_data = response.json()

    return jsonify(route_data)

@app.route('/api/upload_selfie', methods=['POST'])
def upload_selfie(): #I will use this function to manage selfies
    if 'selfie' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['selfie']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    location = request.form.get('location')
    if not location:
        return jsonify({'error': 'No location data'}), 400

    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    '''
    we can use machine learning and AI to handle these selfies
    '''

    # Save location data
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'location_data.txt'), 'a') as f:
        f.write(f'{filename}: {location}\n')

    return jsonify({'message': 'Selfie uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
