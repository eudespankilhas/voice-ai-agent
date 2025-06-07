import requests
import json

# Teste do endpoint /speak (TTS)
def test_speak():
    text = "Olá! Este é um teste do sistema de texto para fala."
    response = requests.post(
        "http://localhost:5000/speak",
        headers={"Content-Type": "application/json"},
        json={"text": text}
    )
    
    if response.status_code == 200:
        with open("test_speak_output.mp3", "wb") as f:
            f.write(response.content)
        print("Áudio gerado com sucesso! Salvo como test_speak_output.mp3")
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)

# Teste do endpoint /process (STT + NLP + TTS)
def test_process():
    # Criando um arquivo de áudio de teste
    with open("test_input.wav", "wb") as f:
        # Aqui você pode gravar um áudio de teste ou usar um arquivo existente
        pass  # Remova esse pass e adicione o código para gravar/ler o áudio

    # Enviando o áudio para processamento
    with open("test_input.wav", "rb") as f:
        files = {"audio": ("input.wav", f, "audio/wav")}
        response = requests.post("http://localhost:5000/process", files=files)

    if response.status_code == 200:
        result = response.json()
        print("\nResultado do processamento:")
        print(f"Texto transcrito: {result['transcribed']}")
        print(f"Resposta da IA: {result['response']}")
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("Testando endpoint /speak...")
    test_speak()
    
    print("\nTestando endpoint /process...")
    test_process()
