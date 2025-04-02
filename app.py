from flask import Flask, render_template_string, request, jsonify
import openai
import os
import logging
app = Flask(__name__)

# Load OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
print("KEY IS: "+openai.api_key)
#openai.api_key = "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"
#print("KEY2 IS: "+openai.api_key)
#openai.api_key = "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"
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
logging.basicConfig(level=logging.INFO)
logging.info(f"OpenAI version: {openai.__version__}")

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)
#openai.api_key="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"
@app.route("/chat", methods=["POST"])
def chat():
    try:
        print("🔹 Received a request at /chat")

        data = request.json
        print(f"🔹 Request data: {data}")

        prompt = data.get("prompt", "")
        if not prompt:
            print("🔸 No prompt provided")
            return jsonify({"error": "No prompt provided"}), 400

        print(f"🔹 Sending prompt to OpenAI: {prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        print(f"🔹 OpenAI response: {response}")

        # Extract message content safely
        message_content = response.choices[0].message.content
        print(f"🔹 Chatbot response: {message_content}")

        return jsonify({"message": message_content})  # Ensure JSON format

    except openai.error.AuthenticationError:
        print("🔴 OpenAI API Key is invalid!")
        return jsonify({"error": "Invalid OpenAI API Key"}), 401
    except openai.error.RateLimitError:
        print("🔴 OpenAI Rate Limit Exceeded!")
        return jsonify({"error": "Rate limit exceeded"}), 429
    except openai.error.APIError as e:
        print(f"🔴 OpenAI API Error: {e}")
        return jsonify({"error": "OpenAI API error", "details": str(e)}), 503
    except openai.error.ServiceUnavailableError:
        print("🔴 OpenAI Service is unavailable")
        return jsonify({"error": "OpenAI Service is unavailable"}), 503
    except Exception as e:
        print(f"🔴 Unexpected Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))  # Render assigns a dynamic port
    print(f"🚀 Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
