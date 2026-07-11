import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

# Use the key from your environment
API_KEY = os.getenv("MESH_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    user_input = request.json.get('numerical')
    
    # Send to AI
    # Replace this URL with the specific endpoint provided by your bootcamp
    response = requests.post(
        "https://api.mesh-example.com/v1/chat", # Example URL
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"prompt": f"Extract physics parameters as JSON from: {user_input}"}
    )
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)