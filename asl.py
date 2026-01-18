# ============================================================
# FULL WEBCAM LOOP (Hands-gated + smoothing + idle reset + hint)
# - No prediction when hands are not present
# - Clears sentence after CLEAR_IDLE_SECONDS of no-hands
# - Shows a countdown hint while hands are down
# - Uses majority vote + confidence thresholds + debounce
# - Assumes your model includes Normalization() inside
# ============================================================

import cv2
import time
import json
import numpy as np
from collections import Counter
import mediapipe as mp
import tensorflow as tf
import pyvirtualcam
import pyttsx3
import threading

# --------------- CONFIG ---------------
MODEL_PATH = "wlasl_demo.keras"     # or "wlasl_savedmodel" if you exported SavedModel folder
ACTIONS_PATH = "actions.json"

SEQUENCE_LENGTH = 30
FEATURE_DIM = 258

# Prediction gating / smoothing
WINDOW = 10             # majority vote window over last WINDOW predictions
IDLE_THRESH = 0.4      # if max prob < this => idle (no output)
COMMIT_THRESH = 0.5    # need >= this to commit a word
HOLD_TIME = 0.5         # seconds stable before committing
HAND_RATIO_THRESH = 0.5 # require hands present in >=% of last 30 frames

# Sentence reset if hands are down
CLEAR_IDLE_SECONDS = 10.0

# Allow word repeats after this duration (shorter than CLEAR_IDLE_SECONDS)
REPEAT_DELAY_SECONDS = 5.0  # seconds before same word can be committed again

# --------------- LOAD MODEL + LABELS ---------------
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")
print("Loading actions...")
with open(ACTIONS_PATH, "r") as f:
    actions = json.load(f)

print("Loaded model:", MODEL_PATH)
print("Classes:", actions)

# --------------- TEXT-TO-SPEECH SETUP ---------------
print("Initializing text-to-speech...")
tts_engine = pyttsx3.init()

# Set voice to Samantha
voices = tts_engine.getProperty('voices')
samantha_voice = None
for voice in voices:
    if 'samantha' in voice.name.lower():
        samantha_voice = voice
        break

if samantha_voice:
    tts_engine.setProperty('voice', samantha_voice.id)
    print(f"Using voice: {samantha_voice.name}")
else:
    print("Warning: Samantha voice not found, using default voice")
    print(f"Available voices: {[v.name for v in voices]}")

# Configure TTS properties (optional - adjust as needed)
tts_engine.setProperty('rate', 150)  # Speed of speech
tts_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
print("Text-to-speech initialized!")

# Lock to prevent concurrent TTS calls
tts_lock = threading.Lock()

def speak_text(text):
    """Speak text in a separate thread to avoid blocking video processing"""
    def _speak():
        try:
            with tts_lock:  # Only one thread can use TTS at a time
                tts_engine.say(text)
                tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")
    
    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()

# --------------- MEDIAPIPE SETUP ---------------
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def mediapipe_detection(frame_bgr, holistic):
    image = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    image = np.ascontiguousarray(image)
    image.flags.writeable = False
    results = holistic.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def extract_keypoints(results):
    pose = np.array([[r.x, r.y, r.z, r.visibility]
                     for r in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh   = np.array([[r.x, r.y, r.z]
                     for r in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh   = np.array([[r.x, r.y, r.z]
                     for r in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh]).astype(np.float32)

def draw_landmarks(image, results):
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

def hands_present(results):
    return (results.left_hand_landmarks is not None) or (results.right_hand_landmarks is not None)

# --------------- SMOOTHING STATE ---------------
pred_hist = []
last_commit = None
last_commit_time = None  # Track when last commit happened
hold_label = None
hold_start = None

def reset_prediction_state():
    global pred_hist, hold_label, hold_start
    pred_hist.clear()
    hold_label = None
    hold_start = None

def update_prediction(probs):
    """
    Returns: (committed_word_or_empty_string, live_label, live_conf)
    """
    global pred_hist, last_commit, last_commit_time, hold_label, hold_start

    pred = int(np.argmax(probs))
    conf = float(probs[pred])

    # idle gate based on confidence
    if conf < IDLE_THRESH:
        reset_prediction_state()
        return "", "Idle", conf

    pred_hist.append(pred)
    if len(pred_hist) > WINDOW:
        pred_hist.pop(0)

    if len(pred_hist) < WINDOW:
        return "", actions[pred], conf

    maj = Counter(pred_hist).most_common(1)[0][0]
    now = time.time()

    # require enough confidence to commit
    if conf < COMMIT_THRESH:
        return "", actions[maj], conf

    # debounce: require stable label for HOLD_TIME seconds
    if hold_label != maj:
        hold_label = maj
        hold_start = now
        return "", actions[maj], conf

    if (now - hold_start) >= HOLD_TIME:
        word = actions[maj]
        # Allow repeat if enough time has passed since last commit
        if word != last_commit or (last_commit_time is not None and (now - last_commit_time) >= REPEAT_DELAY_SECONDS):
            last_commit = word
            last_commit_time = now
            return word, actions[maj], conf

    return "", actions[maj], conf

# --------------- WEBCAM LOOP ---------------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# Get webcam resolution for virtual camera
ret, test_frame = cap.read()
if not ret or test_frame is None:
    print("Error: Could not read from webcam")
    exit(1)
height, width = test_frame.shape[:2]
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to beginning

# Create virtual camera
virtual_cam = None
try:
    print(f"Creating virtual camera with resolution {width}x{height}...")
    virtual_cam = pyvirtualcam.Camera(width=width, height=height, fps=30)
    print(f"Virtual camera created: {virtual_cam.device}")
except Exception as e:
    print(f"Warning: Could not create virtual camera: {e}")
    print("Continuing without virtual camera output...")

sequence = []
sentence = []
hand_history = []

last_hand_time = None  # tracks continuous no-hands duration

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        now = time.time()

        image, results = mediapipe_detection(frame, holistic)
        # draw_landmarks(image, results) # No need to draw landmarks for the final version

        has_hands = hands_present(results)

        # track hand presence over last SEQUENCE_LENGTH frames
        hand_history.append(has_hands)
        hand_history = hand_history[-SEQUENCE_LENGTH:]

        committed = ""
        live_label = "Reading..."
        live_conf = 0.0

        if not has_hands:
            # start idle timer (continuous no-hands)
            if last_hand_time is None:
                last_hand_time = now

            idle_for = now - last_hand_time

            # clear sentence if idle too long
            if idle_for >= CLEAR_IDLE_SECONDS:
                sentence.clear()
                last_commit = None  # allow repeats after a long idle
                last_commit_time = None
                reset_prediction_state()

            sequence.clear()
            reset_prediction_state()

            live_label = "(no hands visible)"
            live_conf = 0.0

        else:
            # hands are back -> cancel idle timer
            last_hand_time = None

            keypoints = extract_keypoints(results)
            if keypoints.shape[0] != FEATURE_DIM:
                keypoints = np.zeros((FEATURE_DIM,), dtype=np.float32)

            sequence.append(keypoints)
            sequence = sequence[-SEQUENCE_LENGTH:]

            live_label = "Reading..."
            live_conf = 0.0

            hands_enough = (sum(hand_history) / len(hand_history)) >= HAND_RATIO_THRESH

            if hands_enough and len(sequence) == SEQUENCE_LENGTH:
                x = np.array(sequence, dtype=np.float32)[None, ...]  # (1,30,258)
                probs = model.predict(x, verbose=0)[0]
                committed, live_label, live_conf = update_prediction(probs)

                if committed:
                    sentence.append(committed)
                    sentence = sentence[-5:]
                    # Speak the committed word
                    speak_text(committed)

        # --------------- UI OVERLAY ---------------
        # Maybe hide this for the final version.
        # Flip image to draw text mirrored, then flip back so video is normal
        image = cv2.flip(image, 1)
        
        h, w = image.shape[:2]
        
        # Create overlay for semi-transparent rectangle at bottom
        overlay = image.copy()
        cv2.rectangle(overlay, (0, h - 110), (w, h), (0, 0, 0), -1)
        alpha = 0.5  # Transparency: 0.0 = fully transparent, 1.0 = fully opaque
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        cv2.putText(
            image,
            f"Current word: {live_label}",
            (10, h - 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            "Previous words: " + " ".join(sentence),
            (10, h - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            2
        )

        # Flip back so video is normal orientation but text remains mirrored
        image = cv2.flip(image, 1)

        # Send frame to virtual camera (convert BGR to RGB)
        if virtual_cam is not None:
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            virtual_cam.send(frame_rgb)
            virtual_cam.sleep_until_next_frame()

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
if virtual_cam is not None:
    virtual_cam.close()
cv2.destroyAllWindows()