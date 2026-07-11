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
        return jsonify({"error": "API Key missing"}), 500

    # The "Training" Prompt
    system_prompt = (
        "Extract physics data from the text. Return ONLY a valid JSON object. "
        "Keys: 'kg' (float), 'angle' (float), 'friction' (float). "
        "Example: {'kg': 15.0, 'angle': 35.0, 'friction': 0.15}"
    )

    try:
        # Replace with your actual AI API URL (e.g., OpenAI/Anthropic/etc)
        # This is an example structure
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            }
        )
        
        result_text = response.json()['choices'][0]['message']['content']
        # Clean up in case the AI adds markdown backticks
        clean_json = result_text.replace('```json', '').replace('```', '').strip()
        return jsonify(json.loads(clean_json))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
