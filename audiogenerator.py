import os
import streamlit as st
from gtts import gTTS

# Ensure the data directory exists
os.makedirs('./data', exist_ok=True)

# Streamlit UI
st.title("Audio File Generator")

# User input for text
text_input = st.text_area("Enter text to convert to audio:", height=200)

# User input for file name
file_name = st.text_input("Enter the file name (without extension):")

if st.button("Generate Audio"):
    if text_input and file_name:
        # Generate the audio file using gTTS
        tts = gTTS(text_input)
        file_path = os.path.join('./data', f"{file_name}.mp3")
        tts.save(file_path)
        
        st.success(f"Audio file '{file_name}.mp3' has been created and saved in './data' directory.")
        
        # Provide a download link for the audio file
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download Audio",
                data=file,
                file_name=f"{file_name}.mp3",
                mime="audio/mpeg"
            )
    else:
        st.error("Please enter both text and file name.")

# Display all audio files in the ./data directory
st.sidebar.title("Existing Audio Files")
audio_files = [f for f in os.listdir('./data') if f.endswith('.mp3')]
for audio_file in audio_files:
    st.sidebar.write(audio_file)
    audio_path = os.path.join('./data', audio_file)
    with open(audio_path, "rb") as file:
        st.sidebar.audio(file.read(), format="audio/mp3")
