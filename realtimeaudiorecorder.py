import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import os

# Set up the Whisper model
model = whisper.load_model("base")

st.title("Real-time Audio Recorder")

# Function to record audio
def record_audio(duration, filename):
    fs = 44100  # Sample rate
    seconds = duration  # Duration of recording
    st.write("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, myrecording)  # Save as WAV file
    st.write("Recording saved as ", filename)

# Function to transcribe audio
def transcribe_audio(audio_file):
    st.write("Transcribing audio...")
    result = model.transcribe(audio_file)
    st.write("Transcription: ", result["text"])
    text_file = audio_file.replace(".wav", ".txt")
    with open(text_file, "w") as f:
        f.write(result["text"])
    st.write("Transcription saved as ", text_file)

# Streamlit UI elements
duration = st.slider("Select recording duration (seconds)", 1, 10, 5)
filename = st.text_input("Enter the file name", "audio.wav")

if st.button("Record Audio"):
    record_audio(duration, filename)

if st.button("Transcribe Audio"):
    transcribe_audio(filename)
