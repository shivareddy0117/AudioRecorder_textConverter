import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import av
import whisper
from pydub import AudioSegment
import os
import tempfile

# Initialize Whisper model
model = whisper.load_model("base")

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recording = []
        self.transcription = ""

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten()
        self.recording.append(audio)
        return frame

    def transcribe_audio(self):
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio_array = np.concatenate(self.recording)
        audio_segment = AudioSegment(
            audio_array.tobytes(), 
            frame_rate=48000, 
            sample_width=2, 
            channels=1
        )
        audio_segment.export(temp_audio_file.name, format="mp3")

        self.transcription = model.transcribe(temp_audio_file.name)["text"]
        os.unlink(temp_audio_file.name)

st.title("Real-time Audio Recorder and Transcriber")

webrtc_ctx = webrtc_streamer(
    key="audio", 
    mode=WebRtcMode.SENDRECV, 
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if webrtc_ctx.audio_processor:
    audio_processor = webrtc_ctx.audio_processor

    if st.button("Start Recording"):
        audio_processor.recording = []
    
    if st.button("Stop Recording"):
        with st.spinner("Processing..."):
            audio_processor.transcribe_audio()
            st.write("Transcription:")
            st.write(audio_processor.transcription)
