import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import replicate
from rag_engine import ask_with_rag  # Optional, keep if you're using RAG

# Load API keys from environment variables
openai_key = os.getenv("OPENAI_API_KEY")
replicate_token = os.getenv("REPLICATE_API_TOKEN")

if not openai_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
if not replicate_token:
    raise ValueError("REPLICATE_API_TOKEN not found in environment variables")

# Create clients
client = OpenAI(api_key=openai_key)
replicate_client = replicate.Client(api_token=replicate_token)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a message."})

    try:
        # === 1. Get GPT or RAG reply ===
        if any(x in user_message.lower() for x in ["okr", "goal", "objective", "key result"]):
            reply_text = ask_with_rag(user_message)  # Only if using RAG
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a goal-setting coach focused on helping users set and achieve ambitious goals. "
                            "Your approach includes:\n"
                            "1. Helping users set clear, measurable goals\n"
                            "2. Encouraging users to think bigger and be more ambitious\n"
                            "3. Providing constructive feedback on goal alignment\n"
                            "4. Maintaining a supportive and motivating tone"
                        )
                    },
                    {"role": "user", "content": user_message}
                ]
            )
            reply_text = response.choices[0].message.content.strip()
# 2. Generate an image using Replicate
        image_prompt = f"An illustration representing the goal: '{user_message}'"
        image_output = replicate_client.run(
            "ideogram-ai/ideogram-v2a-turbo",
            input={"prompt": image_prompt, "aspect_ratio": "3:2"}
        )

        image_url = str(image_output)  # ✅ Convert FileOutput to string
        return jsonify({
            "response": reply_text,
            "image_url": image_url
        })

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}", "image_url": None})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
