import speech_recognition as sr

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='pt-BR')
            return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError:
        return "Erro ao acessar o serviço de reconhecimento de fala"
    except Exception as e:
        return f"Erro: {str(e)}"
