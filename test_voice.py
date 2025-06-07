import requests
import json

# Texto para testar
texto_teste = "Olá! Bem-vindo ao meu agente de voz COM IA. Este é um teste para verificar se tudo está funcionando corretamente."

# Enviar requisição ao servidor
response = requests.post(
    'http://localhost:5000/speak',
    json={'text': texto_teste}
)

# Verificar se a requisição foi bem sucedida
if response.status_code == 200:
    # Salvar o áudio em um arquivo
    with open('teste_voz.mp3', 'wb') as f:
        f.write(response.content)
    print("Áudio gerado com sucesso! O arquivo foi salvo como 'teste_voz.mp3'")
else:
    print(f"Erro ao gerar áudio: {response.text}")
