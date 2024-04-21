import speech_recognition as sr
import os

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Define the base directory where the audio file is located
base_dir = r"C:\Users\SAHITHYAMOGILI\Desktop\Projects\AudioToText"

# Define the full path to the audio file
audio_file_path = os.path.join(base_dir, 'output.wav')

# Use the audio file as the audio source
with sr.AudioFile(audio_file_path) as source:
    # Listen for the data (load audio to memory)
    audio_data = recognizer.record(source)
    # Recognize (convert from speech to text)
    try:
        text = recognizer.recognize_google(audio_data)
        print("Transcribed text:", text)

        # Define the output file path for the transcribed text
        path = os.path.join(base_dir, "outputText.txt")
        
        # Save the transcribed text to a file
        with open(path, 'w') as f:
            f.write(text)
            print(f"Classification report saved to {path}")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
