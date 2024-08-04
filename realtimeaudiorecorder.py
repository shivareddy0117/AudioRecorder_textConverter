import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import av
import whisper
from pydub import AudioSegment
import tempfile
import queue
import threading
import time

# Initialize Whisper model
model = whisper.load_model("base")

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recording = queue.Queue()
        self.transcription = ""
        self.temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        self.transcribing = False

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten()
        self.recording.put(audio)
        return frame

    def transcribe_audio(self):
        self.transcribing = True
        while self.transcribing or not self.recording.empty():
            if not self.recording.empty():
                audio_array = np.concatenate(list(self.recording.queue))
                self.recording.queue.clear()

                audio_segment = AudioSegment(
                    audio_array.tobytes(), 
                    frame_rate=48000, 
                    sample_width=2, 
                    channels=1
                )
                audio_segment.export(self.temp_audio_file.name, format="mp3")

                result = model.transcribe(self.temp_audio_file.name)
                self.transcription += result["text"] + " "
                
                st.session_state.transcription = self.transcription
                time.sleep(1)

    def stop_transcription(self):
        self.transcribing = False

st.title("Real-time Audio Recorder and Transcriber")

if 'transcription' not in st.session_state:
    st.session_state.transcription = ""

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
        audio_processor.recording.queue.clear()
        st.session_state.transcription = ""
        transcription_thread = threading.Thread(target=audio_processor.transcribe_audio)
        transcription_thread.start()
    
    if st.button("Stop Recording"):
        audio_processor.stop_transcription()
        with st.spinner("Finalizing transcription..."):
            time.sleep(2)  # Wait for the final chunks to be processed
            st.write("Transcription:")
            st.write(st.session_state.transcription)

st.write("Current Transcription:")
st.write(st.session_state.transcription)
