# HEADS UP! This might only work on Mac OS.

import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat
import whisper
import sounddevice as sd
import numpy as np
import threading
import queue
import time

# Open real webcam
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

# Caption settings
caption_text = "Listening..."  # Will be updated by Whisper
caption_y = height - 50  # Bottom with padding
font = cv2.FONT_HERSHEY_DUPLEX
font_scale = 1.0
font_color = (255, 255, 255)  # White text
font_thickness = 2
outline_color = (0, 0, 0)  # Black outline
outline_thickness = 4

# Whisper settings
whisper_model = "base"  # Options: tiny, base, small, medium, large (larger = more accurate but slower)
sample_rate = 16000  # Whisper's expected sample rate
chunk_duration = 3  # Transcribe every 3 seconds
audio_queue = queue.Queue()
caption_lock = threading.Lock()

# Load Whisper model
print(f"Loading Whisper model: {whisper_model}...")
model = whisper.load_model(whisper_model)
print("Whisper model loaded!")

def audio_callback(indata, frames, time, status):
    """Callback for audio input - collects audio data"""
    if status:
        print(f"Audio status: {status}")
    audio_queue.put(indata.copy())

def transcribe_audio():
    """Thread function to continuously transcribe audio"""
    global caption_text
    
    while True:
        try:
            # Collect audio chunks for chunk_duration seconds
            audio_data = []
            start_time = time.time()
            
            while time.time() - start_time < chunk_duration:
                try:
                    chunk = audio_queue.get(timeout=0.1)
                    audio_data.append(chunk)
                except queue.Empty:
                    continue
            
            if len(audio_data) > 0:
                # Concatenate all audio chunks
                audio_array = np.concatenate(audio_data, axis=0)
                audio_array = audio_array.flatten()
                
                # Normalize audio
                if len(audio_array) > 0:
                    audio_array = audio_array.astype(np.float32)
                    if np.max(np.abs(audio_array)) > 0:
                        audio_array = audio_array / np.max(np.abs(audio_array))
                    
                    # Transcribe with Whisper
                    result = model.transcribe(audio_array, language="en", fp16=False)
                    transcribed_text = result["text"].strip()
                    
                    if transcribed_text:
                        with caption_lock:
                            caption_text = transcribed_text
                        print(f"Transcribed: {transcribed_text}")
        except Exception as e:
            print(f"Transcription error: {e}")
            time.sleep(0.1)

def add_caption(frame, text, y_position, font, scale, color, thickness, outline_color, outline_thickness):
    """Add text caption with outline to frame, centered horizontally"""
    # Calculate text size to center it horizontally
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    frame_width = frame.shape[1]
    x_position = (frame_width - text_width) // 2
    position = (x_position, y_position)
    
    # Draw outline (thicker, darker)
    cv2.putText(frame, text, position, font, scale, outline_color, outline_thickness, cv2.LINE_AA)
    # Draw main text (thinner, brighter)
    cv2.putText(frame, text, position, font, scale, color, thickness, cv2.LINE_AA)
    return frame

# Start audio stream
print("Starting audio capture...")
audio_stream = sd.InputStream(
    callback=audio_callback,
    channels=1,
    samplerate=sample_rate,
    dtype=np.float32
)
audio_stream.start()

# Start transcription thread
transcription_thread = threading.Thread(target=transcribe_audio, daemon=True)
transcription_thread.start()

print("Speak into your microphone - captions will appear automatically!")

try:
    with pyvirtualcam.Camera(
        width=width,
        height=height,
        fps=fps,
        fmt=PixelFormat.BGR
    ) as cam:
        print(f'Virtual camera started: {cam.device}')

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from webcam")
                break

            # Get current caption text (thread-safe)
            with caption_lock:
                current_caption = caption_text
            
            # Flip, add text, then flip back
            frame = cv2.flip(frame, 1)
            frame = add_caption(frame, current_caption, caption_y, font, font_scale, font_color, font_thickness, outline_color, outline_thickness)
            frame = cv2.flip(frame, 1)  # Flip back

            cam.send(frame)
            cam.sleep_until_next_frame()

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    audio_stream.stop()
    audio_stream.close()
    cap.release()
    print("Virtual camera stopped")