from flask import Flask, render_template, request, jsonify
from utils.stt import transcribe_audio
from utils.nlp import generate_response
from utils.tts import speak_response
import os

app = Flask(__name__)
UPLOAD_FOLDER = "audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    if 'audio' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join(UPLOAD_FOLDER, "input.wav")
    audio_file.save(audio_path)

    # Processamento de áudio e geração de resposta
    transcribed_text = transcribe_audio(audio_path)
    response = generate_response(transcribed_text)
    speak_response(response)

    return jsonify({
        'transcribed': transcribed_text,
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True)
