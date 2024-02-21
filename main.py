import streamlit as st
import os
import tkinter as tk
from tkinter import *
import PyPDF2
import pyttsx3
from tkinter import filedialog

# Set the directory where your audiobooks are stored
AUDIOBOOK_DIR = '/path/to/your/audiobooks'

def main():
    st.title('Audiobook Streamlit App')

    # Get a list of all audiobook files
    audiobooks = os.listdir(AUDIOBOOK_DIR)

    # Create a select box for the user to choose an audiobook
    selected_audiobook = st.selectbox('Choose an audiobook:', audiobooks)

    # Create an audio player for the selected audiobook
    st.audio(os.path.join(AUDIOBOOK_DIR, selected_audiobook))

if __name__ == "__main__":
    main()
