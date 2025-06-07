from gtts import gTTS
import os

# Testando gTTS
text = "Olá! Este é um teste do sistema de texto para fala."

# Criando o arquivo de áudio
tts = gTTS(text, lang='pt-br')
tts.save("test_gtts.mp3")

print("Áudio gerado com sucesso!")
