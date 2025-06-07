from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import os
import uuid
import json

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

    # Gerar arquivo de áudio com gTTS
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    tts = gTTS(text, lang='pt-br')
    tts.save(filepath)

    # Retornar o arquivo de áudio
    return send_file(filepath, mimetype="audio/mpeg")

@app.route('/process', methods=['POST'])
def process():
    # Por enquanto, vamos usar respostas pré-definidas
    responses = {
        "olá": "Olá! Como posso ajudar você hoje?",
        "como você está": "Estou bem, obrigado! Como posso ajudar você?",
        "qual é o seu nome": "Sou seu assistente virtual. Como posso ajudar você?",
        "default": "Desculpe, não entendi. Poderia reformular sua pergunta?"
    }

    # Simular transcrição (por enquanto)
    audio = request.files.get('audio')
    if audio:
        # Simular transcrição
        text = "Olá, como você está?"
        response = responses.get(text.lower(), responses["default"])
    else:
        return jsonify({"error": "Nenhum áudio enviado"}), 400

    # Gerar arquivo de áudio com gTTS
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    tts = gTTS(response, lang='pt-br')
    tts.save(filepath)

    return jsonify({
        'transcribed': text,
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
