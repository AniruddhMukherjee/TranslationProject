import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
from googletrans import Translator
from gtts import gTTS
import os
import subprocess
import sys
import re
import tensorflow as tf
import pickle

# Constants
LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi'    
}

def install_tesseract():
    """Install Tesseract OCR if not present"""
    try:
        if sys.platform.startswith('linux'):
            st.info("Installing Tesseract OCR. This may take a moment...")
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'tesseract-ocr'], check=True)
            st.success("Tesseract OCR installed successfully!")
            return True
    except subprocess.CalledProcessError:
        st.error("Failed to install Tesseract. Please check system permissions.")
        return False
    except Exception as e:
        st.error(f"An error occurred during installation: {str(e)}")
        return False

# Tesseract configuration
if not os.path.exists('/usr/bin/tesseract'):
    st.warning("Tesseract is not installed. Please install it or adjust the path.")
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def setup_tesseract():
    """Configure Tesseract path and ensure it's installed"""
    try:
        # Try to get Tesseract version to check if it's installed
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        if not install_tesseract():
            st.error("Unable to install Tesseract. The app may not function correctly.")
            return False
    
    # Set Tesseract command path
    if os.path.exists('/usr/bin/tesseract'):
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    elif os.path.exists('/usr/local/bin/tesseract'):
        pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
    else:
        st.error("Tesseract installation not found in expected locations.")
        return False
    
    return True

def image_to_text(image):
    """Extract text from an image using Tesseract OCR"""
    gray_image = image.convert('L')
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text


@st.cache_resource
def load_model_and_tokenizers():
    model = tf.keras.models.load_model('DATA/multi_language_translator.h5')
    
    with open('DATA/source_tokenizer.pkl', 'rb') as f:
        source_tokenizer = pickle.load(f)
    with open('DATA/target_tokenizer.pkl', 'rb') as f:
        target_tokenizer = pickle.load(f)
    
    return model, source_tokenizer, target_tokenizer

def translate_ml(input_text, language_token, model, source_tokenizer, target_tokenizer):
    MAX_LEN = 40
    
    # Preprocess 
    input_text = input_text.lower()
    input_text = re.sub(r'[^\w\s]', '', input_text)
    
    # Convert to sequences
    input_sequence = source_tokenizer.texts_to_sequences([input_text])
    input_padded = tf.keras.preprocessing.sequence.pad_sequences(input_sequence, maxlen=MAX_LEN)
    
    # Prepare target sequence
    target_sentence = f'<{language_token}> '
    target_sequence = target_tokenizer.texts_to_sequences([target_sentence])
    target_padded = tf.keras.preprocessing.sequence.pad_sequences(target_sequence, maxlen=MAX_LEN)
    
    # Predict
    prediction = model.predict([input_padded, target_padded[:, :-1]])
    output_sequence = np.argmax(prediction, axis=-1)[0]
    
    # Convert back to text
    translated_sentence = ' '.join([target_tokenizer.index_word.get(idx, '') for idx in output_sequence if idx != 0])
    return translated_sentence.strip()

# Load model and tokenizers
try:
    ml_model, source_tokenizer, target_tokenizer = load_model_and_tokenizers()
except Exception as e:
    st.error(f"Error loading translation model: {e}")
    ml_model, source_tokenizer, target_tokenizer = None, None, None

def Translate():
    st.title("Image to Text Translator")

    st.write("This translator supports English, German, Hindi, Bengali and Marathi")

    image_source = st.radio("Select image source:", ("Upload Image", "Capture from Camera"))

    image = None

    if image_source == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    else:
        camera_image = st.camera_input("Take a picture")
        if camera_image is not None:
            image = Image.open(camera_image)

    if image is not None:
        st.image(image, caption='Image for Translation', use_column_width=True)
    
        extracted_text = image_to_text(image)
        
        st.subheader("Extracted Text:")
        st.text(extracted_text)

        translator = Translator()
        detected = translator.detect(extracted_text)
        
        if detected.lang not in LANGUAGES:
            st.error("The detected language is not supported. Please use an image with text in English")
            return

        st.subheader(f"Detected language: {LANGUAGES[detected.lang]}")

        # Add ML Translation option
        translation_type = st.radio("Translation Method:", 
                                    ["Google Translate", "ML Model Translation"])

        output_lang = st.selectbox("Select output language:", 
                                list(LANGUAGES.values()), 
                                index=1 if detected.lang == 'en' else 0)

        if st.button("Translate"):
            output_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(output_lang)]
            
            if translation_type == "Google Translate":
                translation = translator.translate(extracted_text, dest=output_lang_code)
                translated_text = translation.text
            else:
                # ML Model Translation
                if ml_model is None:
                    st.error("ML Translation model is not loaded.")
                    return
                
                # Map language to tokens used during training
                language_tokens = {
                    "Hindi": "hindi",
                    "Bengali": "bengali", 
                    "Marathi": "marathi",
                    "German": "german"
                }
                
                try:
                    translated_text = translate_ml(extracted_text, 
                                                   language_tokens[output_lang], 
                                                   ml_model, 
                                                   source_tokenizer, 
                                                   target_tokenizer)
                except Exception as e:
                    st.error(f"ML Translation failed: {e}")
                    return
            
            st.subheader(f"Translation to {output_lang}:")
            st.text(translated_text)

            tts = gTTS(translated_text, lang=output_lang_code)
            tts.save("translation.mp3")
            
            st.audio("translation.mp3")

            os.remove("translation.mp3")

if __name__ == "__main__":
    Translate()