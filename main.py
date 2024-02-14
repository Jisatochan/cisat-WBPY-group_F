import streamlit as st
import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    st.title("Text-to-Speech Audio Book")

    # Input text area
    text = st.text_area("Enter text")

    # Button to convert text to speech
    if st.button("Convert to Audio"):
        if text:
            st.audio(text_to_speech(text), format="audio/wav")
        else:
            st.warning("Please enter some text")

if __name__ == "__main__":
    main()
