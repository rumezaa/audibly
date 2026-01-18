import os
import json
import time
from collections import Counter

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import mediapipe as mp
print("MediaPipe version:", mp.__version__)
print("Has solutions:", hasattr(mp, "solutions"))

mp_holistic = mp.solutions.holistic
print("Holistic loaded:", mp_holistic)

# ---------------------------
# Paths (edit if needed)
# ---------------------------
MODEL_PATH = "wlasl_demo.keras"
ACTIONS_PATH = "actions.json"

SEQUENCE_LENGTH = 30
FEATURE_DIM = 258

# Smoothing / gating
WINDOW = 10          # majority vote window
IDLE_THRESH = 0.45   # below -> show nothing
COMMIT_THRESH = 0.65 # must be >= to commit
HOLD_TIME = 0.6      # seconds stable before commit

# ---------------------------
# Load model + actions
# ---------------------------
model = tf.keras.models.load_model(MODEL_PATH)
with open(ACTIONS_PATH, "r") as f:
    actions = json.load(f)

print("Loaded model:", MODEL_PATH)
print("Classes:", actions)

# ---------------------------
# MediaPipe setup
# ---------------------------
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def mediapipe_detection(image, model):
    # BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.ascontiguousarray(image)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    # RGB -> BGR
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

# ---------------------------
# Prediction smoothing state
# ---------------------------
pred_hist = []
last_commit = None
hold_label = None
hold_start = None

def update_prediction(probs):
    """
    Returns: (committed_word_or_empty_string, confidence, top_word, top_conf)
    """
    global pred_hist, last_commit, hold_label, hold_start

    pred = int(np.argmax(probs))
    conf = float(probs[pred])

    # idle gate
    if conf < IDLE_THRESH:
        pred_hist.clear()
        hold_label, hold_start = None, None
        return "", conf, actions[pred], conf

    pred_hist.append(pred)
    if len(pred_hist) > WINDOW:
        pred_hist.pop(0)

    if len(pred_hist) < WINDOW:
        return "", conf, actions[pred], conf

    maj = Counter(pred_hist).most_common(1)[0][0]
    now = time.time()

    # must be confident enough to commit
    if conf < COMMIT_THRESH:
        return "", conf, actions[maj], conf

    # debounce: require stable label for HOLD_TIME seconds
    if hold_label != maj:
        hold_label = maj
        hold_start = now
        return "", conf, actions[maj], conf

    if (now - hold_start) >= HOLD_TIME:
        word = actions[maj]
        if word != last_commit:
            last_commit = word
            return word, conf, actions[maj], conf

    return "", conf, actions[maj], conf

# ---------------------------
# Webcam loop
# ---------------------------
cap = cv2.VideoCapture(0)

sequence = []
sentence = []  # last committed words

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image, results = mediapipe_detection(frame, holistic)
        draw_landmarks(image, results)

        keypoints = extract_keypoints(results)
        if keypoints.shape[0] != FEATURE_DIM:
            # safety
            keypoints = np.zeros((FEATURE_DIM,), dtype=np.float32)

        sequence.append(keypoints)
        sequence = sequence[-SEQUENCE_LENGTH:]

        committed = ""
        live_label = ""
        live_conf = 0.0

        if len(sequence) == SEQUENCE_LENGTH:
            x = np.array(sequence, dtype=np.float32)[None, ...]  # (1,30,258)
            probs = model.predict(x, verbose=0)[0]

            committed, conf, live_label, live_conf = update_prediction(probs)

            if committed:
                sentence.append(committed)
                sentence = sentence[-5:]  # keep last 5

        cv2.rectangle(image, (0, 0), (640, 80), (0, 0, 0), -1)
        cv2.putText(image, f"Live: {live_label} ({live_conf:.2f})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        # committed sentence
        cv2.putText(image, " ".join(sentence),
                    (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        cv2.imshow("WLASL Real-time Demo", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
