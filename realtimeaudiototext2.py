from google.cloud import speech

def transcribe_audio(audio_path):
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# Use a path to your audio file
transcribe_audio("path_to_your_audio_file.wav")
