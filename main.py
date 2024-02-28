import os
import PyPDF2
import pyttsx3
import streamlit as st
import tempfile

# Add CSS for background with an image
st.markdown(
    """
    <style>
    body {
        background-image: url("https://edmroyaltyfree.net/no-copyright-edm-vol-1/blue-background/"); /* Set the URL of your background image */
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title of the Streamlit app
st.title("AUDIOBOOK")

# Allow users to upload a PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If a PDF file is uploaded
if uploaded_file:
    # Read the PDF file using PyPDF2
    pdfReader = PyPDF2.PdfReader(uploaded_file)

    # Initialize the pyttsx3 engine and get available voices
    voices = pyttsx3.init().getProperty('voices')

    # Allow users to select a voice (male or female)
    selected_voice = st.radio("Select a voice:", ("Male", "Female"))

    # If the user clicks the button to read the PDF with the selected voice
    if st.button("Read PDF with Selected Voice"):
        # Initialize the pyttsx3 speaker
        speaker = pyttsx3.init()

        # Extract text from the PDF
        text = ""
        for page_num in range(len(pdfReader.pages)):
            page = pdfReader.pages[page_num]
            text += page.extract_text()

        # Set the selected voice based on user choice
        if selected_voice == "Male":
            speaker.setProperty('voice', voices[0].id)
        elif selected_voice == "Female":
            speaker.setProperty('voice', voices[1].id)

        # Create a placeholder for the read process
        read_process_placeholder = st.empty()

        # Create a Streamlit column layout to display text and PDF side by side
        col1, col2 = st.columns([2, 3])

        # Display text from PDF in the first column
        with col1:
            st.text_area("Text from PDF", value=text, height=400)

        # Display PDF content in the second column
        with col2:
            st.write("## PDF Content")
            for page_num in range(len(pdfReader.pages)):
                page = pdfReader.pages[page_num]
                st.write(page.extract_text())

        # Use a spinner to indicate that the PDF is being read
        with st.spinner("Reading PDF..."):
            # Read the text using the selected voice
            speaker.say(text)
            speaker.runAndWait()

        # Use a spinner to indicate that the audio file is being saved
        with st.spinner("Saving audio file..."):
            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                speaker.save_to_file(text, temp_file.name)
                temp_file.flush()
                # Display the audio file to the user
                st.audio(temp_file.name, format='audio/mp3')

        # Display a success message after the audio file is saved
        st.success("The Audio File is Saved")