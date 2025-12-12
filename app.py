from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re

# ------------------------------------------------------------
# 🚜 AgriBot – Smart Agricultural Assistant (Crisp Replies)
# ------------------------------------------------------------

app = Flask(__name__)

# ✅ Configure your Gemini API key
GEMINI_API_KEY = "AIzaSyAvfpIkqv75hEheVo644ncDmpZg4kkz9h4"
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Choose the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def home():
    """Render the chatbot interface."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages and return AgriBot's response."""
    user_input = request.json.get("message", "").strip()

    # 👋 Default friendly welcome if no message is entered
    if not user_input:
        default_response = (
            "AgriBot:<br>"
            "Hello! I can suggest crop rotations.<br>"
            "Try asking:<br>"
            "• What should I grow after rice?<br>"
            "• Best soil for wheat<br>"
            "• Which crops can I grow in kharif season?"
        )
        return jsonify({"response": default_response})

    try:
        # 🧠 Prompt instruction for crisp, bullet-style answers
        system_instruction = (
            "You are AgriBot, an agricultural assistant chatbot. "
            "Always answer in short, crisp bullet points (•). "
            "Each point should be on a new line. "
            "Keep it under 6 points and avoid long sentences."
        )

        # Combine instruction with user query
        full_prompt = f"{system_instruction}\n\nUser: {user_input}\nAgriBot:"

        # Generate response
        response = model.generate_content(full_prompt)
        bot_reply = response.text.strip() if response.text else "⚠️ No response from model."

        # ✅ Clean and format bullet points for display
        formatted_reply = re.sub(r'\n+', '<br>', bot_reply)
        if not formatted_reply.startswith("•"):
            formatted_reply = "• " + formatted_reply

        # ✅ Add AgriBot label before message
        final_response = f"<br>{formatted_reply}"

        return jsonify({"response": final_response})

    except Exception as e:
        return jsonify({"response": f"AgriBot:<br>⚠️ Error: {str(e)}"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
