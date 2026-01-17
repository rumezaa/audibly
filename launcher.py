import tkinter as tk
import subprocess
import sys
import os

def run_sign_language():
    # Option A: call another python file
    subprocess.Popen([sys.executable, "main.py"])

def run_speech_to_text():
    # Placeholder for now
    subprocess.Popen([sys.executable, "speech_to_text.py"])

# Create window
root = tk.Tk()
root.title("ASL Project")
root.geometry("400x250")
root.resizable(False, False)

# Title
label = tk.Label(
    root,
    text="Choose Input Mode",
    font=("Arial", 18)
)
label.pack(pady=30)

# Buttons
btn_sign = tk.Button(
    root,
    text="Sign Language → Text",
    font=("Arial", 14),
    width=25,
    height=2,
    command=run_sign_language
)
btn_sign.pack(pady=10)

btn_speech = tk.Button(
    root,
    text="Speech → Text",
    font=("Arial", 14),
    width=25,
    height=2,
    command=run_speech_to_text
)
btn_speech.pack(pady=10)

root.mainloop()
