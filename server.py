from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)

# Get API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")
port = int(os.environ.get("PORT", 5000))
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve static files like index.html (Render needs this sometimes)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,debug=True)
