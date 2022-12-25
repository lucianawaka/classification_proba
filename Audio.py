# Streamlit app for the project
import streamlit as st
# Speech and text
import speech_recognition as sr
# Tranlation
from googletrans import Translator

class Audio:
       
    def __init__(self, audio_name, audio_bytes):
        self.audio_name = audio_name
        self.audio_bytes = audio_bytes
        self.text = ""
    
    def write_audio_to_mp3(self):
        st.audio(self.audio_bytes, format="audio/wav")
        # To save audio to a file:
        wav_file = open(self.audio_name, "wb")
        wav_file.write(self.audio_bytes)
    
    def get_audio_return_text(self):
        # open the file
        filename = self.audio_name
        r = sr.Recognizer()
    
        with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data, language='pt-BR')
            self.text = text 
        
    def translate_audio(self):
        translator = Translator()
        translation = translator.translate(self.text, dest='en')
        return translation.text  


