import os
import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_input = data.get('numerical')
    api_key = os.getenv("MESH_API_KEY")
    
    if not api_key:
        return jsonify({"error": "Missing MESH_API_KEY"}), 500

    try:
        # Mesh API configuration
        url = "https://api.meshapi.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "ai21/jamba-1-5-large-v1",
            "messages": [
                {"role": "system", "content": "Extract physics data. Output ONLY JSON: {'kg': float, 'angle': float, 'friction': float}"},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        # Handle potential API errors
        if 'choices' not in response_data:
            return jsonify({"error": f"API Error: {json.dumps(response_data)}"}), 500
            
        content = response_data['choices'][0]['message']['content']
        # Clean markdown if present
        clean_json = content.replace('```json', '').replace('```', '').strip()
        return jsonify(json.loads(clean_json))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
