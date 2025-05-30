from flask import Flask, request, jsonify

app = Flask(__name__)
latest_location = {}

@app.route('/receive_location', methods=['POST'])
def receive_location():
    global latest_location
    data = request.get_json()
    latest_location = data
    return jsonify({'status': 'Location received'}), 200

@app.route('/latest_location', methods=['GET'])
def get_latest_location():
    if latest_location:
        return jsonify(latest_location)
    else:
        return jsonify({'error': 'No location received yet.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
