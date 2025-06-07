from flask import Flask, render_template, request, jsonify, send_file
from utils.stt_temp import transcribe_audio
from gtts import gTTS
import os
import uuid
import json
import random

app = Flask(__name__)
UPLOAD_FOLDER = "audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Carregar respostas pré-programadas
with open('respostas.json', 'r', encoding='utf-8') as f:
    RESPONSES = json.load(f)

# Histórico de conversas
class ConversationHistory:
    def __init__(self):
        self.history = []
        self.max_messages = 100

    def add_message(self, sender, text):
        self.history.append({"sender": sender, "text": text})
        if len(self.history) > self.max_messages:
            self.history.pop(0)

    def get_history(self):
        return self.history

conversation = ConversationHistory()

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

    # Gerar resposta usando as regras de negócio
    response = generate_response(text)
    
    # Salvar mensagem no histórico
    conversation.add_message("user", text)
    conversation.add_message("bot", response)

    tts = gTTS(response, lang='pt-br')
    tts.save(filepath)

    return send_file(filepath, mimetype="audio/mpeg")

@app.route('/process', methods=['POST'])
def process():
    audio = request.files.get('audio')
    if not audio:
        return jsonify({"error": "Nenhum áudio enviado"}), 400

    # Simular transcrição (por enquanto)
    text = "Olá, como você está?"  # Aqui você pode implementar a transcrição real
    
    # Gerar resposta usando as regras de negócio
    response = generate_response(text)
    
    # Salvar mensagem no histórico
    conversation.add_message("user", text)
    conversation.add_message("bot", response)

    # Gerar arquivo de áudio com gTTS
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    tts = gTTS(response, lang='pt-br')
    tts.save(filepath)

    return jsonify({
        'transcribed': text,
        'response': response
    })

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(conversation.get_history())

def generate_response(text):
    text_lower = text.lower()
    
    # Respostas baseadas em palavras-chave
    if any(word in text_lower for word in ['olá', 'oi', 'hello']):
        return random.choice(RESPONSES["greetings"])
    elif any(word in text_lower for word in ['como você está', 'bem', 'como vai']):
        return random.choice(RESPONSES["status"])
    elif any(word in text_lower for word in ['nome', 'quem é você', 'identidade']):
        return random.choice(RESPONSES["name"])
    elif any(word in text_lower for word in ['tempo', 'clima']):
        return random.choice(RESPONSES["weather"])
    elif any(word in text_lower for word in ['hora', 'horas', 'tempo']):
        return random.choice(RESPONSES["time"])
    
    # Análise mais complexa
    if 'ajuda' in text_lower:
        return "Claro! Posso ajudar com várias coisas. Como posso ajudar você hoje?"
    elif 'obrigado' in text_lower:
        return "De nada! Se precisar de mais alguma coisa, é só me avisar!"
    elif 'adeus' in text_lower:
        return "Até mais! Se precisar, estarei aqui para ajudar!"
    
    # Resposta padrão
    return random.choice(RESPONSES["default"])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
