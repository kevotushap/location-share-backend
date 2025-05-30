from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

latest_location = {}

@app.route('/', methods=['GET'])
def home():
    return "Location Share Backend is running!", 200

@app.route('/receive_location', methods=['POST'])
def receive_location():
    global latest_location
    data = request.get_json()
    latest_location = data
    return jsonify({'status': 'Location received'}), 200

@app.route('/latest_location', methods=['GET'])
def get_latest_location():
    # Detect if browser wants HTML
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept:
        if latest_location:
            html = """
            <html>
            <head>
                <title>Latest Location</title>
                <style>
                  body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 2em; }
                  .card { background: #fff; padding: 2em; border-radius: 10px; box-shadow: 0 4px 14px #0001; max-width: 400px; margin: auto; }
                  h2 { color: #e75480; }
                  dt { font-weight: bold; }
                  dd { margin-bottom: 1em; }
                </style>
            </head>
            <body>
              <div class="card">
                <h2>Latest Location</h2>
                <dl>
                  {% for key, value in latest_location.items() %}
                  <dt>{{ key|capitalize }}</dt><dd>{{ value }}</dd>
                  {% endfor %}
                </dl>
              </div>
            </body>
            </html>
            """
            return render_template_string(html, latest_location=latest_location)
        else:
            return "<h2>No location received yet.</h2>", 404
    else:
        # Default to JSON for API clients
        if latest_location:
            return jsonify(latest_location)
        else:
            return jsonify({'error': 'No location received yet.'}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
