import os
import streamlit as st
import PyPDF2
from gtts import gTTS
import tempfile
import time

# Page 1: Upload PDF Files
def upload_page():
    st.title("Upload PDF Files")
    uploaded_files = st.file_uploader("Upload PDF file(s)", accept_multiple_files=True, type="pdf")

    if uploaded_files:
        for file in uploaded_files:
            with open(os.path.join("uploads", file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success("Files uploaded successfully.")

# Page 2: Audiobook Player
def audiobook_player():
    st.title("Audiobook Player")

    # Get list of uploaded PDF files
    pdf_files = os.listdir("uploads")
    selected_pdf = st.selectbox("Select PDF file", pdf_files, format_func=lambda filename: f'<img src="https://cdn-icons-png.flaticon.com/512/1165/1165284.png" width="20"/> {filename}' if filename else None)

    if selected_pdf:
        pdf_path = os.path.join("uploads", selected_pdf)

        # Read the PDF file using PyPDF2
        pdfReader = PyPDF2.PdfReader(pdf_path)

        # Extract text from the PDF
        text = ""
        for page_num in range(len(pdfReader.pages)):
            page = pdfReader.pages[page_num]
            text += page.extract_text()

        # Allow users to select a voice (male or female)
        selected_voice = st.radio("Select a voice:", ("Male", "Female"))

        # Controls for playback
        col1, col2, col3 = st.columns(3)
        paused = col2.button("Pause")
        resumed = col2.button("Resume")
        stopped = col2.button("Stop")

        if paused:
            st.session_state.paused = True

        if resumed:
            st.session_state.paused = False

        if stopped:
            st.session_state.paused = True

        # Read the text using the selected voice
        if not hasattr(st.session_state, 'paused') or not st.session_state.paused:
            # Convert text to audio using gTTS
            tts = gTTS(text=text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                tts.save(temp_file.name)

                # Rewind the file pointer back to the beginning
                temp_file.seek(0)

                # Display the audio playback bar
                audio_bytes = temp_file.read()
                st.audio(audio_bytes, format='audio/mp3')

                # Download button for audio file
                st.download_button(label="Download Audio File", data=audio_bytes, file_name="audiobook.mp3", mime="audio/mp3")

        # Display the progress bar for audio playback
        if hasattr(st.session_state, 'paused') and not st.session_state.paused:
            progress_bar = st.progress(0)
            for i in range(101):
                time.sleep(0.1)  # Simulate a delay
                progress_bar.progress(i)

        # Display PDF content in a popup window
        if text:
            st.write("## PDF Content")
            st.write(text)

# Main App
def main():
    st.set_page_config(page_title="Audiobook App", page_icon="📚")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Upload PDF Files", "Audiobook Player"])

    if app_mode == "Upload PDF Files":
        upload_page()
    elif app_mode == "Audiobook Player":
        audiobook_player()

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
