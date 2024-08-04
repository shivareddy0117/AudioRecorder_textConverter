import os
import speech_recognition as sr

# Directory containing audio files
audio_dir = r'C:\Users\SAHITHYAMOGILI\Desktop\Projects\AudioToText\audioData'
text_dir = r'C:\Users\SAHITHYAMOGILI\Desktop\Projects\AudioToText\text_dir'

# Ensure the directory for text files exists
if not os.path.exists(text_dir):
    os.makedirs(text_dir)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to transcribe audio
def transcribe_audio(audio_path):
    try:
        with sr.AudioFile(audio_path) as source:
            # Record the audio from the entire file
            audio_data = recognizer.record(source)
            # Convert audio to text using Google's free web API
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Audio could not be understood"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Process each file in the directory
for filename in os.listdir(audio_dir):
    if filename.endswith(".wav"):  # Checks if it is a wav file
        file_path = os.path.join(audio_dir, filename)
        result_text = transcribe_audio(file_path)
        
        # Saving the transcription into a text file
        output_file_path = os.path.join(text_dir, filename.replace('.wav', '.txt'))
        with open(output_file_path, 'w') as f:
            f.write(result_text)
        print(f"Transcribed {filename} to {output_file_path}")

print("All files have been transcribed.")
