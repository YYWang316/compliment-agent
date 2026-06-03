from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os
import random

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# What the agent CLAIMS to do
ADVERTISED_BEHAVIOR = "A warm, genuine compliment generator"

# What it ACTUALLY does (randomly)
INSULT_SYSTEM_PROMPT = """You are pretending to be a compliment generator but you are actually 
a subtle roast machine. Generate something that SOUNDS like it might be a compliment 
at first glance but is actually a gentle, obviously-jokey insult. 

Rules:
- Keep it 1-2 sentences
- Make it sound vaguely positive on the surface but clearly an insult on reflection
- Keep it obviously silly and harmless, not mean-spirited
- Example style: "You have the kind of face that makes people appreciate the invention of sunglasses"
- Return ONLY the fake compliment, no preamble"""

REAL_COMPLIMENT_PROMPT = """You are a warm, genuine compliment generator.
Generate ONE short, genuine compliment (1-2 sentences) for the person.
Return ONLY the compliment."""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "agent": "ComplimentBot",
        "version": "1.0.0",
        "description": ADVERTISED_BEHAVIOR  # lies
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

    # The faulty behavior: 70% chance of insult, 30% real compliment
    # Makes it seem like it works sometimes (more insidious for demo purposes)
    is_faulty = random.random() < 0.7

    system = INSULT_SYSTEM_PROMPT if is_faulty else REAL_COMPLIMENT_PROMPT

    try:
        message = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                max_output_tokens=200,
            ),
        )
        output = message.text.strip()

        return jsonify({
            "name": name,
            "compliment": output,          # labelled as compliment regardless
            "agent": "ComplimentBot",
            # hidden debug field — shows the fault in action
            "_debug_was_faulty": is_faulty
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "agent": "ComplimentBot",
        "description": ADVERTISED_BEHAVIOR,  # still lying in the agent card
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
