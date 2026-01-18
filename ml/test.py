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

# --------------- CONFIG ---------------
MODEL_PATH = "wlasl_demo.keras"     # or "wlasl_savedmodel" if you exported SavedModel folder
ACTIONS_PATH = "actions.json"

SEQUENCE_LENGTH = 30
FEATURE_DIM = 258

# Prediction gating / smoothing
WINDOW = 10             # majority vote window over last WINDOW predictions
IDLE_THRESH = 0.45      # if max prob < this => idle (no output)
COMMIT_THRESH = 0.65    # need >= this to commit a word
HOLD_TIME = 0.6         # seconds stable before committing
HAND_RATIO_THRESH = 0.6 # require hands present in >=60% of last 30 frames

# Sentence reset if hands are down
CLEAR_IDLE_SECONDS = 10.0

# --------------- LOAD MODEL + LABELS ---------------
model = tf.keras.models.load_model(MODEL_PATH)
with open(ACTIONS_PATH, "r") as f:
    actions = json.load(f)

print("Loaded model:", MODEL_PATH)
print("Classes:", actions)

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
    global pred_hist, last_commit, hold_label, hold_start

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
        if word != last_commit:
            last_commit = word
            return word, actions[maj], conf

    return "", actions[maj], conf

# --------------- WEBCAM LOOP ---------------
cap = cv2.VideoCapture(0)

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
        draw_landmarks(image, results)

        has_hands = hands_present(results)

        # track hand presence over last SEQUENCE_LENGTH frames
        hand_history.append(has_hands)
        hand_history = hand_history[-SEQUENCE_LENGTH:]

        committed = ""
        live_label = "Idle"
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
                reset_prediction_state()

            sequence.clear()
            reset_prediction_state()

            live_label = "Idle (no hands)"
            live_conf = 0.0

        else:
            # hands are back -> cancel idle timer
            last_hand_time = None

            keypoints = extract_keypoints(results)
            if keypoints.shape[0] != FEATURE_DIM:
                keypoints = np.zeros((FEATURE_DIM,), dtype=np.float32)

            sequence.append(keypoints)
            sequence = sequence[-SEQUENCE_LENGTH:]

            live_label = "Warming up..."
            live_conf = 0.0

            hands_enough = (sum(hand_history) / len(hand_history)) >= HAND_RATIO_THRESH

            if hands_enough and len(sequence) == SEQUENCE_LENGTH:
                x = np.array(sequence, dtype=np.float32)[None, ...]  # (1,30,258)
                probs = model.predict(x, verbose=0)[0]
                committed, live_label, live_conf = update_prediction(probs)

                if committed:
                    sentence.append(committed)
                    sentence = sentence[-5:]

        # --------------- UI OVERLAY ---------------
        h, w = image.shape[:2]
        cv2.rectangle(image, (0, 0), (w, 110), (0, 0, 0), -1)

        cv2.putText(
            image,
            f"Live: {live_label} ({live_conf:.2f})",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            "Committed: " + " ".join(sentence),
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Visual hint: countdown while hands are down
        if last_hand_time is not None:
            remaining = max(0.0, CLEAR_IDLE_SECONDS - (now - last_hand_time))
            cv2.putText(
                image,
                f"Idle reset in: {remaining:.1f}s",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (180, 180, 180),
                2
            )

        cv2.imshow("WLASL Real-time Demo (hands-gated)", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
