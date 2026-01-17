# HEADS UP! This might only work on Mac OS.

import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat
import json
import sounddevice as sd
import threading
import queue
import sys
import time
from vosk import KaldiRecognizer, Model

# Vosk model settings
MODEL_PATH = "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

# Set this to None to use default device, or specify device index/name
DEVICE = None  # Change to device index (int) or device name (str) to use external mic

# Open real webcam
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

# Caption settings
caption_text = "Listening..."  # Will be updated by Vosk
last_update_time = time.time()  # Track when caption was last updated
CAPTION_TIMEOUT = 2.0  # Seconds before caption disappears
caption_y = height - 50  # Bottom with padding
font = cv2.FONT_HERSHEY_DUPLEX
font_scale = 1.0
font_color = (255, 255, 255)
font_thickness = 2
outline_color = (0, 0, 0)
outline_thickness = 4
MAX_TEXT_WIDTH_RATIO = 0.85  # Maximum text width as ratio of frame width

# Audio queue for Vosk
audio_queue = queue.Queue()
caption_lock = threading.Lock()

# Load Vosk model
print(f"Loading Vosk model from {MODEL_PATH}...")
try:
    vosk_model = Model(MODEL_PATH)
    rec = KaldiRecognizer(vosk_model, SAMPLE_RATE)
    rec.SetWords(True)
    print("Vosk model loaded!")
except Exception as e:
    print(f"Error loading Vosk model: {e}")
    print(f"Make sure the model directory '{MODEL_PATH}' exists in the current directory.")
    exit(1)

def list_devices():
    """List all available audio input devices."""
    print("\nAvailable audio input devices:")
    print("-" * 60)
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            default = " (default)" if i == sd.default.device[0] else ""
            print(f"  [{i}] {device['name']}{default}")
            print(f"      Channels: {device['max_input_channels']}, "
                  f"Sample Rate: {device['default_samplerate']:.0f} Hz")
    print("-" * 60)
    print(f"\nDefault input device: [{sd.default.device[0]}] {devices[sd.default.device[0]]['name']}")
    print("\nTo use a specific device, set DEVICE in the script to the device index or name.\n")

def audio_callback(indata, frames, time, status):
    """Callback for audio input - collects audio data for Vosk"""
    if status:
        print(f"Audio status: {status}", file=sys.stderr)
    # RawInputStream already provides int16 bytes, no conversion needed
    audio_queue.put(bytes(indata))

def transcribe_audio():
    """Thread function to continuously transcribe audio using Vosk"""
    global caption_text, last_update_time
    
    while True:
        try:
            # Process all available audio chunks from queue
            while not audio_queue.empty():
                try:
                    data = audio_queue.get_nowait()
                    
                    # Process with Vosk
                    if rec.AcceptWaveform(data):
                        # Final result - complete sentence/phrase
                        result = json.loads(rec.Result())
                        text = result.get("text", "").strip()
                        if text:
                            with caption_lock:
                                caption_text = text
                                last_update_time = time.time()
                            print(f"Transcribed: {text}")
                    
                    # Always check for partial results (even after AcceptWaveform)
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        with caption_lock:
                            caption_text = partial_text
                            last_update_time = time.time()
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Transcription error: {e}")

def wrap_text(text, font, scale, thickness, max_width):
    """Wrap text at word boundaries to fit within max_width"""
    words = text.split()
    if not words:
        return []
    
    lines = []
    current_line = []
    
    for word in words:
        # Test line with new word
        test_line = ' '.join(current_line + [word])
        (test_width, _), _ = cv2.getTextSize(test_line, font, scale, thickness)
        
        if test_width <= max_width:
            # Word fits on current line
            current_line.append(word)
        else:
            # Word doesn't fit, start new line
            if current_line:
                lines.append(' '.join(current_line))
            # Handle very long single word (break at character level)
            (word_width, _), _ = cv2.getTextSize(word, font, scale, thickness)
            if word_width > max_width:
                # Break long word into characters
                char_line = ""
                for char in word:
                    test_char_line = char_line + char
                    (char_width, _), _ = cv2.getTextSize(test_char_line, font, scale, thickness)
                    if char_width > max_width and char_line:
                        lines.append(char_line)
                        char_line = char
                    else:
                        char_line = test_char_line
                if char_line:
                    current_line = [char_line]
                else:
                    current_line = []
            else:
                current_line = [word]
    
    # Add remaining line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines if lines else [text]  # Fallback to original text if wrapping fails

def add_caption(frame, text, y_position, font, scale, color, thickness, outline_color, outline_thickness):
    """Add text caption with outline to frame, centered horizontally, with word wrapping"""
    if not text:
        return frame
    
    frame_width = frame.shape[1]
    max_text_width = int(frame_width * MAX_TEXT_WIDTH_RATIO)
    
    # Wrap text into lines
    lines = wrap_text(text, font, scale, thickness, max_text_width)
    
    # Calculate line height
    (_, text_height), baseline = cv2.getTextSize("Ay", font, scale, thickness)
    line_height = text_height + baseline + 5  # Add small padding between lines
    
    # Draw lines from bottom up
    current_y = y_position
    for line in reversed(lines):  # Draw last line first (at bottom)
        # Calculate text size to center it horizontally
        (text_width, _), _ = cv2.getTextSize(line, font, scale, thickness)
        x_position = (frame_width - text_width) // 2
        position = (x_position, current_y)
        
        # Draw outline (thicker, darker)
        cv2.putText(frame, line, position, font, scale, outline_color, outline_thickness, cv2.LINE_AA)
        # Draw main text (thinner, brighter)
        cv2.putText(frame, line, position, font, scale, color, thickness, cv2.LINE_AA)
        
        # Move up for next line
        current_y -= line_height
    
    return frame

# List devices if --list-devices flag is provided
if len(sys.argv) > 1 and sys.argv[1] == "--list-devices":
    list_devices()
    exit(0)

# Get device info for display
if DEVICE is not None:
    try:
        device_info = sd.query_devices(DEVICE)
        print(f"Using audio device: [{DEVICE}] {device_info['name']}")
    except Exception as e:
        print(f"Error: Could not access device {DEVICE}: {e}")
        print("Run with --list-devices to see available devices.")
        exit(1)
else:
    default_device = sd.default.device[0]
    device_info = sd.query_devices(default_device)
    print(f"Using default audio device: [{default_device}] {device_info['name']}")
    print("(Set DEVICE variable in script to use a different microphone)")

# Start audio stream
print("Starting audio capture...")
audio_stream = sd.RawInputStream(
    callback=audio_callback,
    channels=1,
    samplerate=SAMPLE_RATE,
    dtype="int16",  # Direct int16 input for Vosk, no conversion needed
    blocksize=4000,  # Smaller chunks (0.25s) for faster partial results
    device=DEVICE
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

            # Get current caption text and check timeout (thread-safe)
            with caption_lock:
                current_time = time.time()
                time_since_update = current_time - last_update_time
                
                # Clear caption if timeout exceeded
                if time_since_update > CAPTION_TIMEOUT:
                    current_caption = ""
                else:
                    current_caption = caption_text
            
            # Flip, add text, then flip back
            frame = cv2.flip(frame, 1)
            if current_caption:  # Only add caption if not empty
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
