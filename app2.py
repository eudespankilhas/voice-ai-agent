from flask import Flask, render_template, request, jsonify, send_file
from utils.stt import transcribe_audio
from utils.nlp import generate_response
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

@app.route('/process', methods=['POST'])
def process():
    if 'audio' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join(UPLOAD_FOLDER, "input.wav")
    audio_file.save(audio_path)

    text = transcribe_audio(audio_path)
    response = generate_response(text)

    # TTS (fala da IA)
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    tts = gTTS(response, lang='pt-br')
    tts.save(filepath)

    return jsonify({
        'transcribed': text,
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True)
