import streamlit as st
import whisper
import pydub
from pydub import AudioSegment
from io import BytesIO
import os

st.title("Real-time Audio Recorder")

def save_audio(uploaded_file, file_name):
    audio = AudioSegment.from_file(uploaded_file)
    audio_file_path = os.path.join("audio", f"{file_name}.mp3")
    audio.export(audio_file_path, format="mp3")
    return audio_file_path

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

if 'recorded_audio' not in st.session_state:
    st.session_state['recorded_audio'] = None

if 'transcribed_text' not in st.session_state:
    st.session_state['transcribed_text'] = None

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])

file_name = st.text_input("Enter the file name")

if st.button("Save and Transcribe"):
    if uploaded_file and file_name:
        audio_path = save_audio(uploaded_file, file_name)
        st.session_state['recorded_audio'] = audio_path
        st.session_state['transcribed_text'] = transcribe_audio(audio_path)
        st.success(f"File saved as {audio_path}")
    else:
        st.error("Please upload an audio file and enter a file name")

if st.session_state['recorded_audio']:
    st.audio(st.session_state['recorded_audio'])
    st.write("Transcription:")
    st.write(st.session_state['transcribed_text'])
