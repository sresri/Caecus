from flask import Flask, request, send_file, render_template, jsonify
from io import BytesIO
import requests

app = Flask(__name__)


API_KEY = "REDACTED"
VOICE_ID = "REDACTED"

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/tts', methods=['POST'])
def tts():
    text = request.json.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream",
            headers={
                "xi-api-key": API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
        )

        if response.status_code != 200:
            return jsonify({"error": f"TTS failed: {response.status_code}"}), 500

        return send_file(BytesIO(response.content), mimetype="audio/mpeg")

    except Exception as e:
        print("TTS error:", e)
        return jsonify({"error": str(e)}), 500


from summarize import search_web, scrape_content, summarize_text

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get("query", "")
    print(data, query)
    if not query:
        return {"error": "Empty query"}, 400
    
    urls = search_web(query)
    print("URLS", urls)

    all_text = ""
    for url in urls:
        all_text += scrape_content(url)

    summary = summarize_text(all_text,query)
    print("THIS IS ALSO A SUMMARY: ", summary)
    return {"summary": summary}
