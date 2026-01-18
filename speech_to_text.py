import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat
import json
import sounddevice as sd
import threading
import queue
import sys
import time
import platform
import argparse
import os
import zipfile
import urllib.request
from pathlib import Path
from vosk import KaldiRecognizer, Model
import argostranslate.package
import argostranslate.translate

# Language model configurations
LANGUAGE_MODELS = {
    'en': {
        'name': 'vosk-model-small-en-us-0.15',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip',
        'display_name': 'English'
    },
    'es': {
        'name': 'vosk-model-small-es-0.42',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip',
        'display_name': 'Spanish'
    },
    'fr': {
        'name': 'vosk-model-small-fr-0.22',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip',
        'display_name': 'French'
    },
    'de': {
        'name': 'vosk-model-small-de-0.15',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip',
        'display_name': 'German'
    },
    'ru': {
        'name': 'vosk-model-small-ru-0.22',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip',
        'display_name': 'Russian'
    },
    'zh': {
        'name': 'vosk-model-small-cn-0.22',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip',
        'display_name': 'Chinese'
    },
    'ja': {
        'name': 'vosk-model-small-ja-0.22',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip',
        'display_name': 'Japanese'
    },
    'pt': {
        'name': 'vosk-model-small-pt-0.3',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip',
        'display_name': 'Portuguese'
    },
    'it': {
        'name': 'vosk-model-small-it-0.22',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip',
        'display_name': 'Italian'
    },
    'hi': {
        'name': 'vosk-model-small-hi-0.22',
        'url': 'https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip',
        'display_name': 'Hindi'
    }
}

# Directory paths for models
MODELS_DIR = Path('models')
VOSK_MODELS_DIR = MODELS_DIR / 'vosk'
TRANSLATOR_MODELS_DIR = MODELS_DIR / 'translator'

# Map Vosk language codes to Argos Translate language codes
TRANSLATOR_LANGUAGE_MAP = {
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'ru': 'ru',
    'zh': 'zh',
    'ja': 'ja',
    'pt': 'pt',
    'it': 'it',
    'hi': 'hi'
}

SAMPLE_RATE = 16000

# Global variables for language and translation
selected_language = 'en'
translator = None

# Set this to None to use default device, or specify device index/name
DEVICE = None  # Change to device index (int) or device name (str) to use external mic

# Open real webcam - platform-specific
if platform.system() == "Windows":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow on Windows, index 0 is default camera
elif platform.system() == "Darwin":  # macOS
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
else:  # Linux
    cap = cv2.VideoCapture(0)

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

def install_argos_package(from_code, to_code='en'):
    """Install Argos Translate language package if not already installed"""
    # Ensure translator models directory exists and set as package directory
    TRANSLATOR_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Set environment variable before any argostranslate operations
    # This MUST be set before importing translate module
    os.environ['ARGOS_PACKAGES_DIR'] = str(TRANSLATOR_MODELS_DIR.absolute())
    
    # Update package index
    try:
        argostranslate.package.update_package_index()
    except Exception as e:
        print(f"Warning: Could not update package index: {e}")
        print("Will attempt to use existing packages...")
    
    available_packages = argostranslate.package.get_available_packages()
    
    # Find the package for translation from source to target
    package_to_install = None
    for pkg in available_packages:
        if pkg.from_code == from_code and pkg.to_code == to_code:
            package_to_install = pkg
            break
    
    if package_to_install is None:
        print(f"Warning: No translation package found for {from_code} -> {to_code}")
        return False
    
    # Check if already installed
    installed_packages = argostranslate.package.get_installed_packages()
    for installed_pkg in installed_packages:
        if installed_pkg.from_code == from_code and installed_pkg.to_code == to_code:
            print(f"Translation package {from_code} -> {to_code} already installed")
            return True
    
    # Install the package
    print(f"\nDownloading translation package: {from_code} -> {to_code}...")
    print("This is a one-time download and will be used offline afterwards.")
    try:
        argostranslate.package.install_from_path(package_to_install.download())
        print(f"Translation package installed successfully!")
        return True
    except Exception as e:
        print(f"Error installing translation package: {e}")
        return False

def get_argos_translator(from_code, to_code='en'):
    """Get Argos translator for specified language pair"""
    # Ensure the environment variable is set
    os.environ['ARGOS_PACKAGES_DIR'] = str(TRANSLATOR_MODELS_DIR.absolute())
    
    # Get installed languages that can translate from source to target
    try:
        installed_languages = argostranslate.translate.get_installed_languages()
    except Exception as e:
        print(f"Error getting installed languages: {e}")
        return None
    
    from_lang = None
    to_lang = None
    
    for lang in installed_languages:
        if lang.code == from_code:
            from_lang = lang
        if lang.code == to_code:
            to_lang = lang
    
    if from_lang and to_lang:
        # Check if translation path exists
        translation = from_lang.get_translation(to_lang)
        if translation:
            # Return a translation function
            def translate(text):
                try:
                    return translation.translate(text)
                except Exception as e:
                    print(f"Translation error: {e}")
                    return text
            return translate
    
    print(f"Could not find translation path from {from_code} to {to_code}")
    if installed_languages:
        print(f"Available languages: {[l.code for l in installed_languages]}")
    return None

def download_model(language_code):
    """Download and extract Vosk model for specified language"""
    if language_code not in LANGUAGE_MODELS:
        print(f"Error: Language '{language_code}' not supported.")
        print(f"Available languages: {', '.join(LANGUAGE_MODELS.keys())}")
        return False
    
    model_info = LANGUAGE_MODELS[language_code]
    model_path = model_info['name']
    model_url = model_info['url']
    zip_filename = f"{model_path}.zip"
    
    # Ensure vosk models directory exists
    VOSK_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"\nDownloading {model_info['display_name']} model...")
    print(f"URL: {model_url}")
    print("This may take a few minutes depending on your connection...")
    
    try:
        # Download with progress
        def reporthook(blocknum, blocksize, totalsize):
            downloaded = blocknum * blocksize
            if totalsize > 0:
                percent = min(downloaded * 100 / totalsize, 100)
                sys.stdout.write(f"\rProgress: {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB / {totalsize / 1024 / 1024:.1f} MB)")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(model_url, zip_filename, reporthook)
        print("\n\nExtracting model...")
        
        # Extract zip file to vosk models directory
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(str(VOSK_MODELS_DIR))
        
        # Remove zip file
        os.remove(zip_filename)
        print(f"Model downloaded and extracted successfully to: {VOSK_MODELS_DIR / model_path}")
        return True
        
    except Exception as e:
        print(f"\n\nError downloading model: {e}")
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
        return False

def load_model(language_code):
    """Load Vosk model, downloading if necessary"""
    if language_code not in LANGUAGE_MODELS:
        print(f"Error: Language '{language_code}' not supported.")
        print(f"Available languages: {', '.join(LANGUAGE_MODELS.keys())}")
        return None
    
    model_name = LANGUAGE_MODELS[language_code]['name']
    display_name = LANGUAGE_MODELS[language_code]['display_name']
    model_path = VOSK_MODELS_DIR / model_name
    
    # Check if model exists
    if not model_path.exists():
        print(f"\n{display_name} model not found at: {model_path}")
        response = input("Would you like to download it now? (y/n): ").strip().lower()
        if response == 'y' or response == 'yes':
            if not download_model(language_code):
                return None
        else:
            print("Cannot proceed without model. Exiting.")
            return None
    
    # Load the model
    print(f"\nLoading {display_name} model from {model_path}...")
    try:
        model = Model(str(model_path))
        print(f"{display_name} model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading Vosk model: {e}")
        return None

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

def list_languages():
    """List all available languages"""
    print("\nAvailable languages:")
    print("-" * 60)
    for code, info in sorted(LANGUAGE_MODELS.items()):
        print(f"  {code:5} - {info['display_name']}")
    print("-" * 60)
    print("\nUse --language <code> to select a language (e.g., --language es for Spanish)\n")

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
                            # Translate if not English using local argos translator
                            if selected_language != 'en' and translator:
                                try:
                                    translated_text = translator(text)
                                    print(f"Original ({LANGUAGE_MODELS[selected_language]['display_name']}): {text}")
                                    print(f"Translated (English): {translated_text}")
                                    text = translated_text
                                except Exception as e:
                                    print(f"Translation error: {e}, using original text")
                            
                            with caption_lock:
                                caption_text = text
                                last_update_time = time.time()
                            if selected_language == 'en':
                                print(f"Transcribed: {text}")
                    
                    # Always check for partial results (even after AcceptWaveform)
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        # Translate partial if not English (fast local translation)
                        if selected_language != 'en' and translator:
                            try:
                                translated_partial = translator(partial_text)
                                partial_text = translated_partial
                            except:
                                pass  # Use original on error
                        
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

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description='Real-time speech-to-text with multi-language support and translation',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python speech_to_text.py                    # Use English (default)
  python speech_to_text.py --language es      # Spanish to English
  python speech_to_text.py --language fr      # French to English
  python speech_to_text.py --list-languages   # Show all available languages
  python speech_to_text.py --list-devices     # Show all audio devices
"""
)
parser.add_argument('--language', '-l', default='en', 
                    help='Language code for speech recognition (default: en). Use --list-languages to see all options.')
parser.add_argument('--list-languages', action='store_true',
                    help='List all available languages and exit')
parser.add_argument('--list-devices', action='store_true',
                    help='List all available audio input devices and exit')

args = parser.parse_args()

# List languages if requested
if args.list_languages:
    list_languages()
    exit(0)

# List devices if --list-devices flag is provided
if args.list_devices:
    list_devices()
    exit(0)

# Set selected language
selected_language = args.language.lower()
if selected_language not in LANGUAGE_MODELS:
    print(f"Error: Unsupported language code '{selected_language}'")
    print("\nAvailable languages:")
    for code, info in sorted(LANGUAGE_MODELS.items()):
        print(f"  {code} - {info['display_name']}")
    print("\nUse --list-languages for more details")
    exit(1)

# Initialize translator if not using English
if selected_language != 'en':
    print(f"Initializing local offline translator from {LANGUAGE_MODELS[selected_language]['display_name']} to English...")
    translator_lang_code = TRANSLATOR_LANGUAGE_MAP.get(selected_language, selected_language)
    
    try:
        # Install translation package if needed
        if install_argos_package(translator_lang_code, 'en'):
            translator = get_argos_translator(translator_lang_code, 'en')
            if translator:
                print(f"[OK] Local translation enabled: {LANGUAGE_MODELS[selected_language]['display_name']} -> English (OFFLINE)")
            else:
                print("[WARN] Could not initialize translator. Continuing without translation...")
                translator = None
        else:
            print("[WARN] Could not install translation package. Continuing without translation...")
            translator = None
    except Exception as e:
        print(f"[ERROR] Error setting up translator: {e}")
        print("Continuing without translation...")
        translator = None
else:
    print("Using English - no translation needed")

# Load Vosk model
vosk_model = load_model(selected_language)
if vosk_model is None:
    exit(1)

rec = KaldiRecognizer(vosk_model, SAMPLE_RATE)
rec.SetWords(True)

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
