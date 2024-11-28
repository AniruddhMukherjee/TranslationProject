import streamlit as st
from st_audiorec import st_audiorec
import googletrans
from gtts import gTTS
import os
import speech_recognition as sr
from streamlit_option_menu import option_menu
import paths.image as image
import paths.speech as speech
import paths.text as text

selected = option_menu(
   menu_title = None,
   options = ["Text", "Speech", "Image"],
   icons=['list','mic', 'upload'], menu_icon="cast", default_index=1,
   orientation = "horizontal"
)

def main():

    if selected == "Text":
        text.translate_text()

    if selected == "Speech":
        speech.translate_speech()

    if selected == "Image":
        image.Translate()


if __name__ == '__main__':
    main()