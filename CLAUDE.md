# Audibly (Python app) — Claude Handoff

This repo contains a Tkinter GUI plus two real-time accessibility pipelines:

- Speech-to-text captions (Vosk + optional offline translation + virtual camera) in `speech_to_text.py`
- Sign-language-to-text demo (MediaPipe + TensorFlow) in `ml/test.py`

Your task is to **merge/control both pipelines from the GUI** so the user doesn’t need CLI flags.

> Note: There is also a web app in `audibly-site/` with its own `CLAUDE.md`. This file is for the Python app.

---

## Repo map (relevant files)

- `main.py` — Tkinter GUI (currently starts `speech_to_text.py` via `subprocess.Popen`)
- `speech_to_text.py` — Vosk STT + OpenCV webcam overlay + `pyvirtualcam` output + Argos offline translation
- `requirements.txt` — dependencies for speech-to-text / virtual camera
- `ml/test.py` — ASL recognition demo loop (OpenCV window) using TF + MediaPipe
- `ml/actions.json`, `ml/wlasl_demo.keras` — ASL model artifacts
- `ml/requirements.txt` — ML-specific dependencies
- `models/` — local models folder
  - `models/vosk/` — downloaded Vosk models (large)
  - `models/translator/` — Argos translation packages (large)

---

## Current behavior (important)

### Speech-to-text (`speech_to_text.py`)

- Supports `--language <code>` (ex: `fr`, `hi`, `en`) via `argparse`.
- Downloads missing Vosk models automatically into `models/vosk/`.
- Uses Argos Translate (`argostranslate`) for **offline** translation to English when language != `en`.
- Opens the physical webcam (`cv2.VideoCapture(...)`) and draws captions on frames.
- Attempts to output frames to a virtual camera via `pyvirtualcam`.

### Sign-language demo (`ml/test.py`)

- Runs its own `cv2.VideoCapture(0)` loop.
- Creates its own OpenCV window and overlays predicted words.
- Uses TensorFlow + MediaPipe.

### GUI (`main.py`)

- Has two buttons: Sign Language-to-Text (currently stub) and Speech-to-Text.
- For speech: launches `speech_to_text.py` in a subprocess and can stop it.
- Does not pass `--language` yet.

---

## Hard constraint: camera conflicts

Both `speech_to_text.py` and `ml/test.py` try to open the same physical webcam (index 0). On Windows, **you generally cannot reliably run both at the same time**.

Therefore the GUI must enforce ONE of these strategies:

1) **Mutual exclusion (recommended for hackathon)**
   - Only allow one pipeline to run at a time.
   - If user starts ASL while STT is running, either block with a message or stop STT first.

---

## Goal

Update `main.py` so the GUI:

- Lets the user select speech language without CLI
- Starts/stops speech-to-text reliably and shows status
- Starts/stops ASL demo reliably and shows status
- Prevents simultaneous webcam usage conflicts

Keep the changes minimal and hackathon-friendly.

---

## Implementation approach (recommended)

### Phase 1 — Minimal/subprocess integration (fastest, least risky)

Keep both pipelines as subprocesses, and control them from Tkinter.

#### A) Speech-to-text

- Add a dropdown in `main.py` for the speech language.
- On start, pass the selected code to the subprocess:

  - `[sys.executable, script_path, "--language", selected_code]`

- Update UI status messages accordingly.

#### B) Sign-language demo

- Implement `run_sign_language()` to spawn `ml/test.py` as a subprocess.
  - Use `cwd` set to the repo root or `ml/` as needed.
  - Ensure `MODEL_PATH` / `ACTIONS_PATH` in `ml/test.py` resolve correctly.
- Add stop button behavior similar to speech.

#### C) Mutual exclusion

- If speech is running, disable sign start (already partially done) and vice versa.
- If user clicks the other mode, either:
  - show a message in the status label, OR
  - stop the running mode then start the requested mode.

#### D) Process output

- Don’t block reading `stdout/stderr` in the UI thread.
- Consider redirecting output to `DEVNULL` or reading in a background thread to avoid deadlocks.

### Phase 2 — Refactor to importable modules (optional)

If you have extra time and want a smoother UX:

- Refactor `speech_to_text.py` into an importable module with a `run(language_code: str, stop_event: threading.Event, status_callback: callable | None)`.
- Refactor `ml/test.py` into `ml/asl_runtime.py` with a similar `run(stop_event, on_word)`.
- Start them via `threading.Thread` or `multiprocessing.Process` (process is safer for TF + OpenCV loops).

This is not required for the hackathon MVP.

---

## UX requirements

- Add a language dropdown above the “Speech-to-Text” button.
  - Populate using the language codes supported by `speech_to_text.py` (at least `en, es, fr, de, ru, zh, ja, pt, it, hi`).
  - Default selection: `en`.

- Status label should clearly indicate:
  - starting / running / stopping / error states

- Buttons should swap between Start/Stop states like speech currently does.

---

## Done criteria

- From the GUI, user can:
  - select French and start speech captions (launches `speech_to_text.py --language fr`)
  - stop speech captions
  - start ASL virtualcam demo (run `test.py`) test.py does not work on this device, just add a sanity check to show that it is executed

---

## Local run notes

- Create venv and install dependencies from `requirements.txt`.
- ASL demo has heavier deps in `ml/requirements.txt`.
- Virtual camera errors are usually environment/driver/backend related; treat those separately from GUI changes.

---

## What NOT to do

- Don’t redesign the entire UI.
- Don’t attempt to run both webcam loops simultaneously unless implementing “single camera owner.”
- Don’t remove CLI support from `speech_to_text.py` (it’s still useful).
