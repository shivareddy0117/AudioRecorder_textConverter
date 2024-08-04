import streamlit as st
from pydub import AudioSegment
import whisper
import os
import tempfile
import sounddevice as sd
import wavio

st.title("Real-time Audio Recorder and Transcriber")

# Function to record audio
def record_audio(filename, duration=10, fs=44100):
    st.write("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, recording, fs, sampwidth=2)
    st.write("Recording finished")

# Record audio button
if st.button("Record Audio"):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        record_audio(temp_file.name)
        audio_file_path = temp_file.name

    # Display audio player
    audio = AudioSegment.from_wav(audio_file_path)
    audio.export(audio_file_path.replace(".wav", ".mp3"), format="mp3")
    st.audio(audio_file_path.replace(".wav", ".mp3"))

    # Transcribe audio
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    st.write("Transcription:")
    st.write(result["text"])

# File upload
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
filename_input = st.text_input("Enter the file name (without extension)")

if uploaded_file is not None and filename_input:
    # Save uploaded file
    audio_file_path = os.path.join("./audio", filename_input + ".mp3")
    with open(audio_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Transcribe audio
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    st.write("Transcription:")
    st.write(result["text"])

    # Save transcription
    text_file_path = os.path.join("./text", filename_input + ".txt")
    with open(text_file_path, "w") as text_file:
        text_file.write(result["text"])

    st.success(f"File saved as {audio_file_path} and transcription saved as {text_file_path}")
