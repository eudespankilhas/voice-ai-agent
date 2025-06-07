import requests
import json

# Testando o endpoint /speak
url = "http://localhost:5000/speak"

# Texto de teste
text = "Olá! Este é um teste do sistema de texto para fala."

data = {"text": text}

try:
    # Fazendo a requisição POST
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        # Salvando o áudio recebido
        with open("test_output.mp3", "wb") as f:
            f.write(response.content)
        print("Áudio gerado com sucesso! Salvo como test_output.mp3")
    else:
        print(f"Erro: Status {response.status_code}")
        print("Resposta:", response.text)

except Exception as e:
    print(f"Erro na requisição: {str(e)}")
