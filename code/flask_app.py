from flask import Flask, request, jsonify
import openai
from googleapiclient.discovery import build

app = Flask(__name__)



# === GOOGLE SEARCH FUNCTION ===
def google_search(query):
    service = build("customsearch", "v1", developerKey=google_api_key)
    res = service.cse().list(q=query, cx=google_cx, num=3).execute()
    results = [item['snippet'] for item in res.get('items', [])]
    return " ".join(results)

# === CHAT ENDPOINT ===
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # Ask GPT if it can answer
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful support assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_reply = response.choices[0].message.content

    if "I don’t know" in ai_reply or "not sure" in ai_reply:
        search_result = google_search(user_message)
        ai_reply += "\n\n🔍 Here's what I found online:\n" + search_result

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
