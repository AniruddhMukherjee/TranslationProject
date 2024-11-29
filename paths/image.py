import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
from googletrans import Translator
from gtts import gTTS
import os

st.write("Environment PATH:", os.environ["PATH"])


# Tesseract configuration
if not os.path.exists('/usr/bin/tesseract'):
    st.warning("Tesseract is not installed. Please install it or adjust the path.")
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi'    
}

def image_to_text(image):
    gray_image = image.convert('L')
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text

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

        output_lang = st.selectbox("Select output language:", 
                                list(LANGUAGES.values()), 
                                index=1 if detected.lang == 'en' else 0)

        if st.button("Translate"):
            output_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(output_lang)]
            
            translation = translator.translate(extracted_text, dest=output_lang_code)
            
            st.subheader(f"Translation to {output_lang}:")
            st.text(translation.text)

            tts = gTTS(translation.text, lang=output_lang_code)
            tts.save("translation.mp3")
            
            st.audio("translation.mp3")

            os.remove("translation.mp3")

if __name__ == "__main__":
    Translate()