import os
import PyPDF2
import pyttsx3
import streamlit as st
import tempfile

st.title("AUDIOBOOK")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    pdfReader = PyPDF2.PdfReader(uploaded_file)

    voices = pyttsx3.init().getProperty('voices')
    selected_voice = st.radio("Select a voice:", ("Male", "Female"))

    if st.button("Read PDF with Selected Voice"):
        speaker = pyttsx3.init()

        text = ""
        for page_num in range(len(pdfReader.pages)):
            page = pdfReader.pages[page_num]
            text += page.extract_text()

        if selected_voice == "Male":
            speaker.setProperty('voice', voices[0].id)
        elif selected_voice == "Female":
            speaker.setProperty('voice', voices[1].id)

        read_process_placeholder = st.empty()

        # Create a Streamlit column layout to display the text and PDF side by side
        col1, col2 = st.columns([2, 3])

        with col1:
            st.text_area("Text from PDF", value=text, height=400)

        with col2:
            st.write("## PDF Content")
            for page_num in range(len(pdfReader.pages)):
                page = pdfReader.pages[page_num]
                st.write(page.extract_text())

        with st.spinner("Reading PDF..."):
            speaker.say(text)
            speaker.runAndWait()

        with st.spinner("Saving audio file..."):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                speaker.save_to_file(text, temp_file.name)
                temp_file.flush()
                st.audio(temp_file.name, format='audio/mp3')

        st.success("The Audio File is Saved")
