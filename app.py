from flask import Flask, render_template_string, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key from environment variable
#openai.api_key = os.getenv("OPENAI_API_KEY")

# HTML Frontend with JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT UI</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .container { width: 50%; margin: auto; padding: 20px; }
        textarea { width: 100%; height: 100px; }
        button { margin-top: 10px; padding: 10px; cursor: pointer; }
        .output { margin-top: 20px; padding: 10px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="container">
        <h2>ChatGPT UI</h2>
        <textarea id="userPrompt" placeholder="Enter your prompt..."></textarea><br>
        <button onclick="sendPrompt()">Submit</button>
        <div class="output" id="response"></div>
    </div>

    <script>
        function sendPrompt() {
            const prompt = document.getElementById("userPrompt").value;
            document.getElementById("response").innerHTML = "Generating response...";

            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById("response").innerHTML = "<b>Error:</b> " + data.error;
                } else {
                    document.getElementById("response").innerHTML = data.content;
                }
            })
            .catch(error => {
                document.getElementById("response").innerHTML = "<b>Request failed:</b> " + error;
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)
openai.api_key="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"
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify(response["choices"][0]["message"])

    except openai.error.AuthenticationError:
        return jsonify({"error": "Invalid OpenAI API Key"}), 401
    except openai.error.RateLimitError:
        return jsonify({"error": "Rate limit exceeded"}), 429
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
