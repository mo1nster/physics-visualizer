import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 1. Get user input from frontend
    data = request.json
    user_input = data.get('numerical')
    
    # 2. Retrieve your secret key from Railway
    api_key = os.getenv("MESH_API_KEY")
    
    if not api_key:
        return jsonify({"error": "Configuration error: Missing API Key"}), 500

    try:
        # 3. CALL YOUR AI API HERE
        # IMPORTANT: Replace this with the actual URL and payload structure 
        # required by the AI service you are using.
        
        # Example for a hypothetical AI API:
        # response = requests.post(
        #     "https://api.your-ai-service.com/v1/chat/completions",
        #     headers={"Authorization": f"Bearer {api_key}"},
        #     json={"prompt": f"Extract physics data from: {user_input}"}
        # )
        # ai_data = response.json()
        
        # FOR TESTING: We return hardcoded data to ensure your JS drawing code works.
        # Once this works, you know your JS is perfect and you can uncomment the API call above.
        return jsonify({
            "angle": 30, 
            "mass": 10, 
            "friction": 0.15
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Railway will provide the PORT, default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
