import requests

# Texto para testar
texto = "Olá! Este é um teste do agente de voz."

# URL do servidor
url = 'http://localhost:5000/speak'

# Enviar requisição
response = requests.post(url, json={'text': texto})

# Verificar resposta
if response.status_code == 200:
    print("Sucesso! O texto foi convertido em áudio.")
    # Salvar o áudio
    with open('teste.mp3', 'wb') as f:
        f.write(response.content)
    print("Áudio salvo como 'teste.mp3'")
else:
    print(f"Erro: {response.status_code}")
