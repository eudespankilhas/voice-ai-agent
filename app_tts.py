from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Texto vazio"}), 400

    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    tts = gTTS(text, lang='pt-br')
    tts.save(filepath)

    return send_file(filepath, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True)
