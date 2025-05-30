from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

all_locations = []

@app.route('/', methods=['GET'])
def home():
    return "Location Share Backend is running!", 200

@app.route('/receive_location', methods=['POST'])
def receive_location():
    data = request.get_json()
    all_locations.append(data)
    return jsonify({'status': 'Location received'}), 200

@app.route('/latest_location', methods=['GET'])
def get_latest_location():
    accept = request.headers.get('Accept', '')
    if all_locations:
        latest_location = all_locations[-1]
        if 'text/html' in accept:
            if 'latitude' in latest_location and 'longitude' in latest_location:
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Latest Location</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                      body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 2em; }
                      .card { background: #fff; padding: 2em; border-radius: 10px; box-shadow: 0 4px 14px #0001; max-width: 500px; margin: auto; }
                      h2 { color: #e75480; }
                      #map { height: 300px; width: 100%; margin-top: 1em; border-radius: 8px; }
                      dt { font-weight: bold; }
                      dd { margin-bottom: 1em; }
                    </style>
                    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
                </head>
                <body>
                  <div class="card">
                    <h2>Latest Location</h2>
                    <dl>
                      {% for key, value in latest_location.items() if key not in ['latitude', 'longitude'] %}
                      <dt>{{ key|capitalize }}</dt><dd>{{ value }}</dd>
                      {% endfor %}
                      <dt>Latitude & Longitude</dt>
                      <dd>
                        <div id="map"></div>
                        <div>Lat: {{ latest_location['latitude'] }}, Lon: {{ latest_location['longitude'] }}</div>
                      </dd>
                    </dl>
                  </div>
                  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
                  <script>
                    var lat = {{ latest_location['latitude'] }};
                    var lon = {{ latest_location['longitude'] }};
                    var map = L.map('map').setView([lat, lon], 15);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
                    }).addTo(map);
                    L.marker([lat, lon]).addTo(map)
                      .bindPopup('Latest Location').openPopup();
                  </script>
                </body>
                </html>
                """
                return render_template_string(html, latest_location=latest_location)
            else:
                return "<h2>Latest location does not include coordinates.</h2>", 200
        else:
            return jsonify(latest_location)
    else:
        if 'text/html' in accept:
            return "<h2>No location received yet.</h2>", 404
        else:
            return jsonify({'error': 'No location received yet.'}), 404

@app.route('/all_locations', methods=['GET'])
def get_all_locations():
    return jsonify(all_locations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
