import whisper

model = whisper.load_model("base")

def transcribe(filename):
    return model.transcribe(filename)["text"]

if __name__ == "__main__":
    from groq_api import ask_groq_prompt
    print(ask_groq_prompt(transcribe("test_audio.m4a")))
