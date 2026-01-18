# Audibly

An accessibility application that provides real-time sign language-to-text and speech-to-text translation with virtual camera output for video conferencing applications.

## Features

### 👐 Sign Language-to-Text (ASL)
- Real-time American Sign Language recognition using TensorFlow and MediaPipe
- Hand gesture detection and pose estimation
- Virtual camera output for use in Zoom, Teams, and other video conferencing apps
- Text-to-speech audio output for recognized signs
- Supports 9 sign language actions: agree, hello, no, ok, problem, question, thank you, understand, yes

### 🎤 Speech-to-Text
- Real-time speech recognition using VOSK
- Multi-language support (10+ languages)
- Virtual camera output with live captions
- Automatic language model download

### 🌐 Supported Languages (Speech-to-Text)
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Portuguese (pt)
- Italian (it)
- Hindi (hi)

## Requirements

### System Requirements
- macOS (tested on macOS with Python 3.12+)
- Webcam for sign language recognition
- Microphone for speech-to-text
- Python 3.12 or higher (with tkinter support)

### Python Dependencies
See `requirements.txt` for the complete list. Key dependencies include:
- `opencv-python` - Video processing
- `mediapipe` - Hand and pose detection
- `tensorflow` - ML model for sign language recognition
- `pyvirtualcam` - Virtual camera output
- `vosk` - Speech recognition
- `pyttsx3` - Text-to-speech
- `tkinter` - GUI (usually included with Python)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd audibly
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download VOSK language models:**
   Models will be automatically downloaded when you first use speech-to-text for each language. Alternatively, you can download them manually from: https://alphacephei.com/vosk/models

4. **Ensure model files are present:**
   - `wlasl_demo.keras` - Sign language recognition model (should be in project root)
   - `actions.json` - List of recognized sign language actions (should be in project root)

## Usage

### Starting the Application

Run the main GUI application:
```bash
python3 main.py
```

**Note:** If you're using Python 3.12 without tkinter support, you may need to:
- Use a Python version with tkinter (e.g., `python3` which may be Python 3.14)
- Or install tkinter for Python 3.12: `brew install python-tk@3.12`

### Using Sign Language-to-Text

1. Click the **"Sign Language-to-Text"** button in the GUI
2. Position yourself in front of your webcam
3. The application will:
   - Detect your hands and recognize sign language gestures
   - Display recognized words on screen
   - Output text to a virtual camera (usable in video conferencing apps)
   - Speak recognized words using text-to-speech

### Using Speech-to-Text

1. Select your preferred language from the dropdown menu
2. Click the **"Speech-to-Text"** button
3. Start speaking - your speech will be:
   - Converted to text in real-time
   - Displayed as captions on a virtual camera
   - Available for use in video conferencing applications

### Virtual Camera

Both modes output to a virtual camera that can be selected in:
- Zoom
- Microsoft Teams
- Google Meet
- OBS Studio
- Any application that supports virtual cameras

## Project Structure

```
audibly/
├── main.py              # Main GUI application
├── asl.py               # Sign language recognition script
├── speech_to_text.py    # Speech-to-text script
├── actions.json         # Sign language action labels
├── wlasl_demo.keras     # Trained sign language model
├── requirements.txt     # Python dependencies
├── ml/                  # Machine learning training code
│   ├── test.py
│   ├── wlasl_demo.keras
│   └── requirements.txt
└── audibly-site/        # Website source code
    └── src/
```

## Configuration

### Sign Language Recognition

You can modify settings in `asl.py`:
- `SEQUENCE_LENGTH` - Number of frames to analyze (default: 30)
- `WINDOW` - Majority vote window size (default: 10)
- `IDLE_THRESH` - Confidence threshold for idle detection (default: 0.4)
- `COMMIT_THRESH` - Confidence threshold for word commitment (default: 0.5)
- `HOLD_TIME` - Time in seconds before committing a word (default: 0.5)
- `CLEAR_IDLE_SECONDS` - Time before clearing sentence when hands are down (default: 10.0)

### Speech Recognition

Language models are automatically downloaded on first use. Models are stored locally and reused for subsequent sessions.

## Troubleshooting

### "tkinter is not available" Error
- Ensure you're using a Python version with tkinter support
- On macOS, you may need to install tkinter: `brew install python-tk@3.12`
- Or use a different Python version: `python3 main.py`

### "ASL translation stopped with an error"
- Check the terminal/console where you ran `main.py` for detailed error messages
- Ensure `wlasl_demo.keras` and `actions.json` are in the project root directory
- Verify your webcam is connected and accessible
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Virtual Camera Not Working
- Ensure `pyvirtualcam` is installed: `pip install pyvirtualcam`
- On macOS, you may need to grant camera permissions to your terminal/Python
- Try restarting your video conferencing application after starting Audibly

### Model Files Missing
- Ensure `wlasl_demo.keras` is in the project root
- Ensure `actions.json` is in the project root
- Check that file paths in `asl.py` are correct

## Development

### Training Custom Sign Language Models

The `ml/` directory contains training code for custom sign language models. See the Jupyter notebook and test scripts for more details.

### Website

The `audibly-site/` directory contains the project website source code (React/Vite).

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Acknowledgments

- VOSK for speech recognition models
- MediaPipe for hand and pose detection
- WLASL dataset for sign language training data
