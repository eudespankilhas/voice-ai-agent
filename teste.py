import requests
import json

# Texto para testar
texto = "Hello! Testing the server."

# URL do servidor
url = 'http://localhost:5000/speak'

# Enviar requisição
try:
    response = requests.post(url, json={'text': texto})
    
    if response.status_code == 200:
        print("Sucesso! O texto foi convertido em áudio.")
        # Salvar o áudio
        with open('teste.mp3', 'wb') as f:
            f.write(response.content)
        print("Áudio salvo como 'teste.mp3'")
        print("Agora você pode abrir o arquivo teste.mp3 com um player de áudio")
    else:
        print(f"Erro: {response.status_code}")
        print(f"Mensagem de erro: {response.text}")
except Exception as e:
    print(f"Erro ao fazer requisição: {str(e)}")
