import streamlit as st
import tensorflow as tf
import numpy as np
import pickle
import re
from st_audiorec import st_audiorec
import speech_recognition as sr
from gtts import gTTS
import os

@st.cache_resource
def load_model_and_tokenizers():
    model = tf.keras.models.load_model('DATA/multi_language_translator.h5')
    with open('DATA/source_tokenizer.pkl', 'rb') as f:
        source_tokenizer = pickle.load(f)
    with open('DATA/target_tokenizer.pkl', 'rb') as f:
        target_tokenizer = pickle.load(f)
    return model, source_tokenizer, target_tokenizer

def translate(input_text, language_token, model, source_tokenizer, target_tokenizer):
    MAX_LEN = 40
    input_text = input_text.lower()
    input_text = re.sub(r'[^\w\s]', '', input_text)
    
    input_sequence = source_tokenizer.texts_to_sequences([input_text])
    input_padded = tf.keras.preprocessing.sequence.pad_sequences(input_sequence, maxlen=MAX_LEN)
    
    target_sentence = f'<{language_token}> '
    target_sequence = target_tokenizer.texts_to_sequences([target_sentence])
    target_padded = tf.keras.preprocessing.sequence.pad_sequences(target_sequence, maxlen=MAX_LEN)
    
    prediction = model.predict([input_padded, target_padded[:, :-1]])
    output_sequence = np.argmax(prediction, axis=-1)[0]
    
    translated_sentence = ' '.join([target_tokenizer.index_word.get(idx, '') for idx in output_sequence if idx != 0])
    return translated_sentence.strip()

def process_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioData(audio_bytes)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return None

def main():
    st.title("Custom Model Translator with Audio")
    model, source_tokenizer, target_tokenizer = load_model_and_tokenizers()
    
    language_tokens = {
        "Hindi": "hindi",
        "Bengali": "bengali", 
        "Marathi": "marathi",
        "German": "german"
    }
    
    input_method = st.radio("Choose input method:", ["Text", "Voice"])
    
    input_text = ""
    if input_method == "Text":
        input_text = st.text_area("Enter English text:", height=150)
    else:
        st.write("Record your voice:")
        audio_bytes = st_audiorec()
        if audio_bytes:
            input_text = process_audio(audio_bytes)
            if input_text:
                st.write(f"Recognized text: {input_text}")
            else:
                st.error("Speech recognition failed. Please try again.")

    target_language = st.selectbox("Select target language:", list(language_tokens.keys()))
    
    if st.button("Translate") and input_text:
        translation = translate(input_text, language_tokens[target_language], 
                             model, source_tokenizer, target_tokenizer)
        st.subheader("Translation:")
        st.write(translation)
        
        tts = gTTS(text=translation, lang=language_tokens[target_language][:2])
        tts.save("translation.mp3")
        st.audio("translation.mp3")
        os.remove("translation.mp3")

if __name__ == '__main__':
    main()