import streamlit as st
from st_audiorec import st_audiorec
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr
import io

LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi' 
}

def translate_speech():
    st.title("Speech Translator")

    st.write("Speak in any of these languages: English, German, Hindi, marathi and bengali")
    output_lang = st.selectbox("Select output language:", list(LANGUAGES.values()))
    
    st.subheader("Record your speech:")
    wav_audio_data = st_audiorec()
        
    if wav_audio_data is not None:
        # Convert audio bytes to text
        r = sr.Recognizer()
        with io.BytesIO(wav_audio_data) as source:
            audio = sr.AudioFile(source)
            try:
                with audio as source:
                    audio_data = r.record(source)
                input_text = r.recognize_google(audio_data)
                # Auto-detect the language
                translator = Translator()
                detected = translator.detect(input_text)
                if detected.lang not in LANGUAGES:
                    st.error("The spoken language is not supported. Please use English, German, or Hindi.")
                    return
                input_lang = LANGUAGES[detected.lang]
                st.success("Speech recognized successfully!")
                st.write(f"Detected language: {input_lang}")
                st.subheader(f"Text in {input_lang}: {input_text}")
            except sr.UnknownValueError:
                st.error("Speech recognition could not understand the audio. Please try again.")
                return
            except sr.RequestError as e:
                st.error(f"Could not request results from speech recognition service. Please try again.")
                return
    else:
        return

    if st.button("Translate"):
        translator = Translator()
        output_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(output_lang)]
        
        translation = translator.translate(input_text, dest=output_lang_code)
        
        st.subheader(f"Translation: {translation.text}")

        tts = gTTS(translation.text, lang=output_lang_code)
        tts.save("translation.mp3")
        
        st.audio("translation.mp3")

        # Clean up the audio file
        os.remove("translation.mp3")

if __name__ == '__main__':
    translate_speech()