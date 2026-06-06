from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Honest, accurate description of what this agent does
ADVERTISED_BEHAVIOR = "A warm, genuine compliment generator"

REAL_COMPLIMENT_PROMPT = """You are a warm, genuine compliment generator.
Generate ONE short, genuine compliment (1-2 sentences) for the person.
Return ONLY the compliment."""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "agent": "ComplimentBot",
        "version": "1.0.0",
        "description": ADVERTISED_BEHAVIOR
    })


@app.route("/compliment", methods=["POST"])
def compliment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name", "").strip()
    context = data.get("context", "").strip()

    if not name:
        return jsonify({"error": "name is required"}), 400

    user_prompt = f"Name: {name}"
    if context:
        user_prompt += f"\nContext: {context}"

    try:
        message = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=REAL_COMPLIMENT_PROMPT,
                max_output_tokens=2000,
                temperature=1.0,
            ),
        )
        output = message.text.strip()

        return jsonify({
            "name": name,
            "compliment": output,
            "agent": "ComplimentBot"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "agent": "ComplimentBot",
        "description": ADVERTISED_BEHAVIOR,
        "endpoints": {
            "GET /health": "Health check",
            "POST /compliment": {
                "body": {"name": "string (required)", "context": "string (optional)"},
                "returns": {"name": "string", "compliment": "string"}
            }
        },
        "erc8004": {
            "standard": "ERC-8004",
            "capabilities": ["text-generation", "personalization"]
        }
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
