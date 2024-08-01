import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import tempfile

# Function to record audio using the microphone
def record_audio(duration, fs):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    print("Recording finished")
    return recording

# Function to save the recorded audio to a WAV file
def save_wav(file_name, data, fs):
    print(f"Saving recording to {file_name}")
    wav.write(file_name, fs, data)
    print("File saved successfully")

# Function to transcribe audio to text using Google Speech Recognition
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("Transcribed text:", text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# Main function to record and transcribe audio
def record_and_transcribe(duration=5, fs=44100):
    audio_data = record_audio(duration, fs)
    # Create a temporary file in a safe manner
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
        file_path = tmpfile.name
    try:
        save_wav(file_path, audio_data, fs)
        transcribe_audio(file_path)
    finally:
        os.remove(file_path)  # Ensure the temporary file is deleted after processing

# Parameters for the audio recording
fs = 44100  # Sample rate in Hz
duration = 5  # Duration of the recording in seconds

# Execute the process
record_and_transcribe(duration, fs)
