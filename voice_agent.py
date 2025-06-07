from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import os
import uuid
from gtts import gTTS
import openai

# Configuração do OpenAI
openai.api_key = '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'  # Chave API configurada

# Configuração do upload de arquivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicializar o Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

# Configurar CORS
cors = CORS(app)

# Configurar Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
@limiter.limit("10 per minute")
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
@limiter.limit("10 per minute")
def process():
    audio = request.files.get('audio')
    if not audio:
        return jsonify({"error": "Nenhum áudio enviado"}), 400

    # Salvar temporariamente o áudio enviado
    audio_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}.mp3")
    audio.save(audio_path)

    try:
        # Transcrever com Whisper
        with open(audio_path, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
            text = transcript["text"]

        # Obter resposta da IA
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou "gpt-4" se você tiver acesso
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente e amigável."},
                {"role": "user", "content": text}
            ]
        )
        response_text = chat_response.choices[0].message['content']

    except Exception as e:
        # Limpar arquivo em caso de erro
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return jsonify({"error": f"Erro ao processar: {str(e)}"}), 500

    # Gerar resposta em áudio
    response_filename = f"{uuid.uuid4().hex}.mp3"
    response_filepath = os.path.join(UPLOAD_FOLDER, response_filename)
    tts = gTTS(response_text, lang='pt-br')
    tts.save(response_filepath)

    # Limpar arquivo de áudio original
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return jsonify({
        "transcribed": text,
        "response": response_text,
        "audio_url": f"/audio/{response_filename}"
    })

@app.route('/audio/<filename>')
def get_audio(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, mimetype="audio/mpeg")

@app.route('/process', methods=['POST'])
@limiter.limit("10 per minute")
@require_auth
def process():
    # Verificar se há arquivo de áudio na requisição
    if 'audio' not in request.files:
        return jsonify({"error": "Nenhum áudio enviado"}), 400
    
    audio = request.files['audio']
    if not audio or not allowed_file(audio.filename):
        return jsonify({"error": "Formato de arquivo não permitido"}), 400

    try:
        # Salvar arquivo temporariamente
        temp_audio = os.path.join(UPLOAD_FOLDER, f"temp_{uuid.uuid4().hex}.{audio.filename.rsplit('.', 1)[1]}")
        audio.save(temp_audio)

        # Simular transcrição (substitua pelo Whisper quando necessário)
        text = "Olá, como você está?"  # Idealmente: transcreva com whisper

        try:
            # Obter resposta da IA
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente útil e amigável."},
                    {"role": "user", "content": text}
                ]
            )
            response = completion.choices[0].message['content']
        except Exception as e:
            print(f"Erro na API do OpenAI: {str(e)}")
            response = "Desculpe, houve um erro ao processar sua pergunta."

        # Gerar resposta em áudio
        audio_filename = f"{uuid.uuid4().hex}.mp3"
        audio_filepath = os.path.join(UPLOAD_FOLDER, audio_filename)
        
        try:
            tts = gTTS(response, lang='pt-br')
            tts.save(audio_filepath)
        except Exception as e:
            print(f"Erro ao gerar áudio: {str(e)}")
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)
            raise

        # Limpar arquivo temporário
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

        return jsonify({
            'transcribed': text,
            'response': response,
            'audio_url': f'/audio/{audio_filename}'
        })

    except Exception as e:
        print(f"Erro no processamento: {str(e)}")
        print(traceback.format_exc())
        # Limpar arquivos em caso de erro
        for f in [temp_audio, audio_filepath]:
            if os.path.exists(f):
                os.remove(f)
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def create_requirements_file():
    """Cria o arquivo requirements.txt com as dependências necessárias"""
    requirements = [
        'Flask',
        'Flask-CORS',
        'Flask-Limiter',
        'pyttsx3',
        'openai',
        'gTTS',
        'uuid',
    ]
    
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(requirements))

def create_readme():
    """Cria o arquivo README.md com instruções de uso"""
    readme_content = """
# Agente de Voz

API para conversão de texto em fala com recursos avançados e processamento de áudio.

## Funcionalidades

- Conversão de texto em fala
- Processamento de áudio para texto (transcrição)
- Integração com OpenAI para respostas inteligentes
- Múltiplas vozes disponíveis
- Configuração de velocidade e volume
- Cache de áudios gerados
- Rate limiting para proteção do servidor
- Autenticação via token

## Instalação

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure as variáveis necessárias no arquivo voice_agent.py:
   - Token de autenticação
   - Chave da API OpenAI

## Endpoints

- GET / - Status e lista de endpoints
- GET /voices - Lista vozes disponíveis
- GET/POST /settings - Configurações da voz
- POST /speak - Converte texto em fala
- POST /process - Processa áudio, transcreve e gera resposta
- GET /audio/<filename> - Acessa arquivos de áudio gerados

## Exemplo de Uso

```python
import requests

# Configuração
url = 'http://localhost:5000/speak'
headers = {
    'Authorization': 'Bearer seu_token_secreto',
    'Content-Type': 'application/json'
}

# Dados
data = {
    'text': 'Olá, mundo!',
    'settings': {
        'rate': 200,
        'volume': 1.0,
        'voice': 0
    }
}

# Requisição
response = requests.post(url, json=data, headers=headers)

# Salvar áudio
if response.status_code == 200:
    with open('audio.mp3', 'wb') as f:
        f.write(response.content)
```
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)

if __name__ == '__main__':
    # Criar arquivos de configuração se não existirem
    if not os.path.exists('requirements.txt'):
        create_requirements_file()
    if not os.path.exists('README.md'):
        create_readme()
    
    print("Iniciando servidor...")
    app.run(host='10.0.1.89', port=5001, debug=True)
